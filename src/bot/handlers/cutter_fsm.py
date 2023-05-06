import os

from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text

from bot.keyboards.user_keyboard import get_ikb, get_kb
from bot.serveces.engine.main import start_calculate
from bot.serveces.payment import check_payment, get_label
from bot.states.cutter_states import CutterState


async def cut_type_command(message: types.Message):
    await CutterState.cut_type.set()
    await message.answer(
        "Выберите тип резца",
        reply_markup=get_kb("Круглый", "Призматический", "Отменить")
    )


async def common_cancel_handler(message: types.Message):
    await message.answer("Выберите услугу",
                         reply_markup=get_kb("Рассчитать резец",
                                             "Рассчитать протяжку"
                                             )
                         )
    await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply("Расчет отменен", reply_markup=get_kb(
        "Рассчитать резец",
        "Рассчитать протяжку"
    )
                        )


async def cut_type_invalid(message: types.Message):
    await message.reply(
        "Я не знаю такого резца. 🤷‍♀️ Выберите тип резца из представленных",
        reply_markup=get_kb("Круглый", "Призматический", "Отменить")
    )


async def cut_type_valid(message: types.Message, state: FSMContext):
    await CutterState.cut_data.set()
    async with state.proxy() as data:
        data["object_type"] = f"Резец - {message.text}"

    await message.answer(
        f"Укажите данные резца в формате\n"
        f"{'D1/D2/D3/D4/R/l1/l2/l3/L/f' if message.text == 'Круглый' else 'D/D1/l1/l2/l3/L/f'}\n"
        f"Например так: {'20/16/18/10/15/3/1/5/20/0.5' if message.text == 'Круглый' else '30/35/3/10/20/25/0.5'}\n"
        f"Размерности и пробелы ставить не нужно",
        reply_markup=get_kb("Отменить")
    )


async def cut_data_invalid(message: types.Message):
    await message.reply(
        f"Вы где-то ошиблись. 🤔 Введите корректные данные\nВы ввели: {message.text}",
    )


async def cut_data_valid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        length = len(message.text.split("/"))
        cut_type = data["object_type"].split(" - ")[1]

        if length == 7 and cut_type == "Круглый":
            return await message.reply(f"Вы где-то ошиблись. 🤔 Введите корректные данные\nВы ввели: {message.text}")
        elif length == 10 and cut_type == "Призматический":
            return await message.reply(f"Вы где-то ошиблись. 🤔 Введите корректные данные\nВы ввели: {message.text}")
        else:
            values = [el.replace(",", ".") for el in message.text.split("/")]
            round_symbols = ["D1", "D2", "D3", "D4", "R", "l1", "l2", "l3", "L", "f"]
            prismatic_symbols = ["D", "D1", "l1", "l2", "l3", "L", "f"]
            values_dict = dict(
                zip(round_symbols if cut_type == "Круглый" else prismatic_symbols, values)
            )
            output_values = [f"{item[0]}={item[1]}\n" for item in values_dict.items()]
            label = get_label()
            data["label"] = label
            data["chat_id"] = message.chat.id
            data["output"] = output_values

            for key, value in values_dict.items():
                if value.isdigit():
                    data[key] = int(value)
                else:
                    data[key] = float(value)
            await message.answer(
                f"Данные верны? 👀\nЧто считаем: {data['object_type']}\nРазмеры резца:\n{''.join(output_values)}"
                f"\nЧтобы бот смог приступить к расчету, сперва необходимо оплатить 💰",
                reply_markup=get_ikb(
                    [f"cutter success {'paid' if check_payment(label) else 'not paid'}",
                     "cutter fail"
                     ],
                    label=label,
                    service_type="cutter"
                )
            )


async def cutter_not_paid_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(
            f"Данные верны? 👀\nСчитаем:\n{data['object_type']}\nРазмеры резца:\n{''.join(data['output'])}"
            f"\nЧтобы бот смог приступить к расчету, сперва необходимо оплатить  💰",
            reply_markup=get_ikb(
                [f"cutter success {'paid' if check_payment(data['label']) else 'not paid'}",
                 "cutter fail"
                 ],
                label=data["label"],
                service_type="cutter"
            )
        )
    await callback.answer(
        "Чтобы бот смог приступить к расчету, сперва необходимо провести оплату (нажмите кнопку 'оплатить')",
        show_alert=True
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()


async def cutter_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == "cutter success paid" and check_payment(data["label"]):
            await callback.answer("Приступил к расчетам. Ожидайте...", show_alert=True)
            start_calculate(data)
            file_name = f"./{'solved_cutter_circle' if 'Круглый' in data['object_type'] else 'solved_cutter_prismatic'}_{callback.message.chat.id}.txt"
            with open(file_name, "rb") as file:
                await callback.message.reply_document(file, "rb")

            os.remove(file_name)
        else:
            await callback.answer("Расчет отменен ❌", show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=None)
        await state.finish()


def register_cutter_handlers(dp: Dispatcher):
    """Registers cutter handlers"""
    dp.register_message_handler(cut_type_command, Text(equals="Рассчитать резец", ignore_case=True))
    dp.register_message_handler(common_cancel_handler, Text(equals="отменить", ignore_case=True))
    dp.register_message_handler(
        cancel_handler,
        Text(equals="отменить", ignore_case=True),
        state="*"
    )
    dp.register_message_handler(
        cut_type_invalid,
        lambda message: message.text not in ["Круглый", "Призматический"],
        state=CutterState.cut_type
    )
    dp.register_message_handler(cut_type_valid, state=CutterState.cut_type)
    dp.register_message_handler(
        cut_data_invalid,
        lambda message: len(message.text.split("/")) not in [7, 10] or not all(
            el.replace(",", ".").replace(".", "").isdigit() for el in message.text.split("/")),
        state=CutterState.cut_data
    )
    dp.register_message_handler(cut_data_valid, state=CutterState.cut_data)
    dp.register_callback_query_handler(
        cutter_not_paid_callback,
        lambda callback: callback.data and "not paid" in callback.data,
        state=CutterState.cut_data
    )
    dp.register_callback_query_handler(
        cutter_callback,
        lambda callback: callback.data and callback.data.startswith("cutter"),
        state=CutterState.cut_data
    )

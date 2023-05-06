import os
import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.keyboards.user_keyboard import get_ikb, get_kb
from bot.serveces.engine.main import start_calculate
from bot.serveces.payment import check_payment, get_label
from bot.states.broach_states import BroachState


async def broach_data_command(message: types.Message):
    await BroachState.broach_data.set()
    await message.answer(
        "Укажите данные вашей протяжки в формате:\nz/d/D/b/f/Tf/r/L(длина протяжки)"
        "\nНапример так: 6/26/30/6/0.3/0.2/0.2/30\nРазмерности и пробелы ставить не нужно",
        reply_markup=get_kb("Отменить")
    )


async def broach_data_invalid(message: types.Message):
    await message.reply(
        f"Вы где-то ошиблись. 🤔 Введите корректные данные.\nВы ввели: {message.text}",
        reply_markup=get_kb("Отменить")
    )


async def broach_data_valid(message: types.Message, state: FSMContext):
    variants = ['6x23x26x6x0.3x0.2x0.2',    '6x26x30x6x0.3x0.2x0.2',     '6x28x32x7x0.3x0.2x0.2',     '8x32x36x6x0.4x0.2x0.3',
                 '8x36x40x7x0.4x0.2x0.3',    '8x42x46x8x0.4x0.2x0.3',     '8x46x50x9x0.4x0.2x0.3',     '8x52x58x10x0.5x0.3x0.5',
                 '8x56x62x10x0.5x0.3x0.5',   '8x62x68x12x0.5x0.3x0.5',    '10x72x78x12x0.5x0.3x0.5',   '10x82x88x12x0.5x0.3x0.5',
                 '10x92x98x14x0.5x0.3x0.5',  '10x102x108x16x0.5x0.3x0.5', '10x112x120x18x0.5x0.3x0.5', '6x11x14x3x0.3x0.2x0.2',
                 '6x13x16x3.5x0.3x0.2x0.2',  '6x16x20x4x0.3x0.2x0.2',     '6x18x22x5x0.3x0.2x0.2',     '6x21x25x5x0.3x0.2x0.2',
                 '6x23x28x6x0.3x0.2x0.2',    '6x26x32x6x0.4x0.2x0.3',     '6x28x34x7x0.4x0.2x0.3',     '8x32x38x6x0.4x0.2x0.3',
                 '8x36x42x7x0.4x0.2x0.3',    '8x42x48x8x0.4x0.2x0.3',     '8x46x54x9x0.5x0.3x0.5',     '8x52x60x10x0.5x0.3x0.5',
                 '8x56x65x10x0.5x0.3x0.5',   '8x62x72x12x0.5x0.3x0.5',    '10x72x82x12x0.5x0.3x0.5',   '10x82x92x12x0.5x0.3x0.5',
                 '10x92x102x14x0.5x0.3x0.5', '10x102x112x16x0.5x0.3x0.5', '10x112x125x18x0.5x0.3x0.5', '10x16x20x2.5x0.3x0.2x0.2',
                 '10x18x23x3x0.3x0.2x0.2',   '10x21x26x3x0.3x0.2x0.2',    '10x23x29x4x0.3x0.2x0.2',    '10x26x32x4x0.4x0.2x0.3',
                 '10x28x35x4x0.4x0.2x0.3',   '10x32x40x5x0.4x0.2x0.3',    '10x36x45x5x0.4x0.2x0.3',    '10x42x52x6x0.4x0.2x0.3',
                 '10x46x56x7x0.5x0.3x0.5'
                ]

    values = [el.replace(",", ".") for el in message.text.split("/")]

    if "x".join(values[:7]) not in variants:
        return await message.reply(f"Вы где-то ошиблись. 🤔 Введите корректные данные\nВы ввели: {message.text}")
    else:
        broach_symbols = ["n", "d", "D", "b", "f", "Tf", "r", "L"]
        values_dict = dict(zip(broach_symbols, values))
        output_values = [f"{item[0]}={item[1]}\n" for item in values_dict.items()]

        async with state.proxy() as data:
            data["object_type"] = "Протяжка"
            label = data.get("label") if data.get("label") else get_label()

            for key, value in values_dict.items():
                if value.isdigit():
                    data[key] = int(value)
                else:
                    data[key] = float(value)

            data["stanok"] = "7510"
            data["chat_id"] = message.chat.id
            data["label"] = label
            data["output"] = output_values

        await message.answer(
            f"Данные верны? 👀\nРазмеры протяжки:\n{''.join(output_values)}\n"
            f"Чтобы бот смог приступить к расчету, сперва необходимо оплатить 💰",
            reply_markup=get_ikb(
                [f"broach success {'paid' if check_payment(label) else 'not paid'}",
                 "broach fail"
                 ],
                label=label,
                service_type="broach"
            )
        )


async def broach_not_paid_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(
            f"Данные верны? 👀\nРазмеры протяжки:\n{''.join(data['output'])}\n"
            f"Чтобы бот смог приступить к расчету, сперва необходимо оплатить  💰",
            reply_markup=get_ikb(
                [f"broach success {'paid' if check_payment(data['label']) else 'not paid'}",
                 "broach fail"
                 ],
                label=data["label"],
                service_type="broach"
            )
        )
    await callback.answer(
        "Чтобы бот смог приступить к расчету, сперва необходимо провести оплату (нажмите кнопку 'оплатить')",
        show_alert=True
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()


async def broach_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        if callback.data == "broach success paid" and check_payment(data["label"]):
            await callback.answer("Приступил к расчетам. Ожидайте...", show_alert=True)
            start_calculate(data)

            with open(f"./solved_broach_{callback.message.chat.id}.txt", "rb") as file:
                await callback.message.reply_document(file, "rb")

            os.remove(f"./solved_broach_{callback.message.chat.id}.txt")
        else:
            await callback.answer("Расчет отменен ❌", show_alert=True)

        await callback.message.edit_reply_markup(reply_markup=None)
        await state.finish()
        print(data)


def register_broach_handlers(dp: Dispatcher):
    """Registers broach handlers"""
    dp.register_message_handler(broach_data_command, Text(equals="Рассчитать протяжку", ignore_case=True))
    dp.register_message_handler(
        broach_data_invalid,
        lambda message: len(message.text.split("/")) != 8 or not all(
            el.replace(",", ".").replace(".", "").isdigit() for el in message.text.split("/")),
        state=BroachState.broach_data
    )
    dp.register_message_handler(broach_data_valid, state=BroachState.broach_data)
    dp.register_callback_query_handler(
        broach_not_paid_callback,
        lambda callback: callback.data and "not paid" in callback.data,
        state=BroachState.broach_data
    )
    dp.register_callback_query_handler(
        broach_callback,
        lambda callback: callback.data and callback.data.startswith("broach"),
        state=BroachState.broach_data
    )

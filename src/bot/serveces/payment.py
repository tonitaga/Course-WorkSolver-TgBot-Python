import os
import random
from string import ascii_lowercase, ascii_uppercase

from dotenv import load_dotenv
from yoomoney import Client, Quickpay


def get_label(length: int = 16) -> str:
    letters = ascii_lowercase + ascii_uppercase
    numbers = "".join(map(str, range(10)))
    symbols = letters + numbers
    return "".join([random.choice(symbols) for _ in range(length)])


def check_payment(label: str) -> bool:
    load_dotenv('.env')
    yoomoney_token = os.getenv("YOOMONEY_TOKEN")

    client = Client(yoomoney_token)
    history = client.operation_history(label=label)
    return True if [operation.status for operation in history.operations] == ["success"] else False


def get_quickpay_form(label: str, service_type: str):

    load_dotenv('.env')
    wallet = os.getenv("WALLET")

    quickpay = Quickpay(
        receiver=wallet,
        quickpay_form="shop",
        targets="Оплата расчета",
        paymentType="SB",
        sum=300 if service_type == 'cutter' else 400,
        label=label
    )
    return quickpay

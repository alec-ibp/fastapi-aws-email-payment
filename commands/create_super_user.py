import asyncclick as click
import databases
from pydantic import EmailStr

from managers.user import UserManager
from db.init_db import database
from models import RoleType


@click.command()
@click.option("-f", "--firstname", type=str, required=True)
@click.option("-l", "--lastname", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-pw", "--password", type=str, required=True)
async def create_user(firstname: str, lastname: str, email: EmailStr, phone, iban, password):
    user_data = {"firstname": firstname, "lastname": lastname, "email": email,
                 "phone": phone, "iban": iban, "password": password, "role": RoleType.admin}

    await database.connect()
    await UserManager.register(user_data)

    await database.disconnect()


if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")

import sqlalchemy
from db.init_db import metadata
from models.enums import RoleType



user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("email", sqlalchemy.String(126), unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("firstname", sqlalchemy.String(126), nullable=False),
    sqlalchemy.Column("lastname", sqlalchemy.String(126), nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String(126), nullable=True),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleType), nullable=False, server_default=RoleType.complainer.name),
    sqlalchemy.Column("iban", sqlalchemy.String(200)),
)

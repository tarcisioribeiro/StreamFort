import os
from dotenv import load_dotenv

load_dotenv()

absolute_app_path = os.getcwd()
backup_sh_path: str = "services/backup.sh"

menu_options = ["Selecione uma opção", "Senhas", "Arquivos", "Cartões", "Contas Bancárias"]

server_config = """
[server]
headless = true
enableStaticServing = true
"""

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_NAME")

db_config = {
    "host": db_host,
    "port": db_port,
    "user": db_user,
    "password": db_password,
    "database": db_database,
}

field_names: list = ["Site", "Link", "Login", "Senha"]

to_remove_list: list = ["'", ")", "(", ",", "Decimal", "[", "]", "\\", "datetime.date"]
to_remove_archive_list: list = [
    "'",
    ")",
    "(",
    ",",
    "Decimal",
    "[",
    "]",
    "datetime.date",
]

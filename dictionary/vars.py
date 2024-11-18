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
bank_account_field_names: list = ["Nome", "Agência", "Número da Conta", "Senha bancária", "Senha digital"]

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

financial_institution_list = ['Mercado Pago', 'Itaú', 'Nubank', 'Bradesco', 'Sicoob', 'C6 Bank', 'Banco do Brasil', 'Pagbank', 'Picpay']
financial_institution_list.sort()
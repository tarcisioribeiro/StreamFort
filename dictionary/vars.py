"""
Variáveis globais da aplicação.
"""

import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

absolute_app_path = os.getcwd()

operational_system = os.name

dark_theme = '''[theme]
primaryColor="#bd93f9"
backgroundColor="#282a36"
secondaryBackgroundColor="#44475a"
textColor="#f8f8f2"'''

light_theme = """[theme]
primaryColor = "#61afef"
backgroundColor = "#fefefe"
secondaryBackgroundColor = "#e6e6e6"
textColor = "#3c4048"
"""

server_config = """
[server]
headless = true
enableStaticServing = true"""

server_config = """
[server]
headless = true
enableStaticServing = true
"""

today = datetime.now()
today = today.date()
actual_horary = datetime.now().strftime("%H:%M:%S")
actual_year = today.year
actual_year = str(actual_year)
actual_month = today.month
next_month = actual_month + 1
first_month_day = datetime(today.year, today.month, 1)
first_month_day = first_month_day.date()
today = str(today)
first_month_day = str(first_month_day)

db_host = os.getenv("DB_HOSTNAME")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_NAME")

db_config = {
    "host": db_host,
    "port": db_port,
    "user": db_user,
    "password": db_password,
    "database": db_database
}

field_names = [
    "Site",
    "Link",
    "Login",
    "Senha"
]

bank_account_field_names = [
    "Nome",
    "Agência",
    "Número da Conta",
    "Senha bancária",
    "Senha digital"
]

to_remove_list = [
    "'",
    ")",
    "(",
    ",",
    "Decimal",
    "[",
    "]",
    "\\",
    "datetime.date"
]

to_remove_archive_list = [
    "'",
    ")",
    "(",
    ",",
    "Decimal",
    "[",
    "]",
    "datetime.date",
]

financial_institution_list = [
    'Mercado Pago',
    'Itaú',
    'Nubank',
    'Bradesco',
    'Sicoob',
    'C6 Bank',
    'Banco do Brasil',
    'Pagbank',
    'Picpay'
]

financial_institution_list.sort()

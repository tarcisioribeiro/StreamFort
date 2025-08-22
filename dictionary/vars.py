import os
from dotenv import load_dotenv

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

bank_account_field_names = [
    "Nome",
    "Agência",
    "Número da Conta",
    "Senha bancária",
    "Senha digital",
]

financial_institution_list = [
    "Mercado Pago",
    "Itaú",
    "Nubank",
    "Bradesco",
    "Sicoob",
    "C6 Bank",
    "Banco do Brasil",
    "Pagbank",
    "Picpay",
]

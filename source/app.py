import streamlit as st
from data.session_state import logged_user
from dictionary.vars import menu_options
from functions.login import User
from functions.query_executor import QueryExecutor
from source.archives import Archives
from source.bank_accounts import BankAccount
from source.credit_cards import CreditCards
from source.homepage import Home
from source.passwords import Passwords
from source.configuration.main import Configuration
from time import sleep


def logout():
    st.session_state.is_logged_in = False
    st.rerun()

def HomePage():

    sidebar = st.sidebar

    with sidebar:
        call_user = User()
        name, sex = call_user.check_user()
        call_user.show_user(name, sex)

    sidebar_menu_dictionary = {
        "Selecione uma opção": Home(),
        "Senhas": Passwords(),
        "Arquivos": Archives(),
        "Cartões": CreditCards(),
        "Contas Bancárias": BankAccount(),
        "Configurações": Configuration()
    }

    sidebar_choice = st.sidebar.selectbox(label="Menu", options=sidebar_menu_dictionary.keys())

    sidebar.divider()

    sidebar_reload_button = sidebar.button(label=":cd: Recarregar")
    sidebar_logoff_button = sidebar.button(label=":lock: Sair")

    if sidebar_reload_button:
        with sidebar:
            with st.spinner(text="Recarregando..."):
                sleep(2.5)
                st.rerun()

    if sidebar_logoff_button:

        with sidebar:
            query_executor = QueryExecutor()
            log_query = '''INSERT INTO seguranca.logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES ( %s, %s, %s);'''
            log_values = (logged_user, "Logoff", "O usuário realizou logoff.")
            query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

            with st.spinner("Aguarde um momento..."):    
                sleep(2.5)
                st.toast("Saindo do sistema...")
                sleep(2.5)
                logout()

    if sidebar_choice:
        call_interface = sidebar_menu_dictionary[sidebar_choice]
        call_interface.main_menu()

    elif sidebar.button(label=":lock: Sair"):
        with sidebar:
            with st.spinner("Aguarde um momento..."):
                sleep(2.5)
                st.toast("Saindo do sistema...")
                sleep(2.5)
                logout()

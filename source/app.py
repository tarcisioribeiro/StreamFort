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

    sidebar_choice = st.sidebar.selectbox(
        label="Menu",
        options=list(menu_options),
    )

    sidebar.divider()

    sidebar_home_button = sidebar.button(label=":house: Início")
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
                sleep(1)
                st.toast("Saindo do sistema...")
                sleep(1)
                logout()

    if sidebar_choice == "Selecione uma opção" or sidebar_home_button:
        call_home_page = Home()
        call_home_page.show_home_page()

    elif sidebar_choice == "Senhas":
        passwords = Passwords()
        passwords.interface()

    elif sidebar_choice == "Arquivos":

        call_archives = Archives()
        call_archives.main_menu()

    elif sidebar_choice == "Cartões":
        call_credit_card = CreditCards()
        call_credit_card.main_menu()

    elif sidebar_choice == "Contas Bancárias":
        bank_account = BankAccount()
        bank_account.main_menu()

    elif sidebar.button(label=":lock: Sair"):
        with sidebar:
            with st.spinner("Aguarde um momento..."):
                sleep(1)
                st.toast("Saindo do sistema...")
                sleep(1)
                logout()

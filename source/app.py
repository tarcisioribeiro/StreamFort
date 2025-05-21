import streamlit as st
from dictionary.sql.other_queries import delete_session_query
from dictionary.user_data import user_id, user_document
from functions.login import Login
from functions.query_executor import QueryExecutor
from source.archives import Archives
from source.bank_accounts import BankAccount
from source.credit_cards import CreditCards
from source.homepage import Home
from source.passwords import Passwords
from source.configuration.main import Configuration
from source.utilities.main import Utilities
from source.configuration.help import Help
from time import sleep


def logout():
    """
    Realiza o logout da aplicação, deletando os registros de sessão do usuário.
    """

    QueryExecutor().insert_query(
        query=delete_session_query,
        values=(user_id, user_document),
        success_message="Logout efetuado.",
        error_message="Erro ao efetuar logout:"
    )

    with st.spinner("Aguarde um momento..."):
        sleep(1.25)
        st.toast("Saindo do sistema...")
        sleep(1.25)

    st.session_state.is_logged_in = False
    st.rerun()


def HomePage():
    """
    Exibe a barra lateral e seu menu de opções.
    """
    sidebar = st.sidebar

    with sidebar:
        name, sex = Login().check_user(user_id, user_document)
        Login().show_user(name, sex)

    sidebar_menu_dictionary = {
        "Início": Home(),
        "Senhas": Passwords(),
        "Arquivos": Archives(),
        "Cartões": CreditCards(),
        "Contas Bancárias": BankAccount(),
        "Configurações": Configuration(),
        "Utilitários": Utilities()
    }

    sidebar_choice = st.sidebar.selectbox(
        label="Menu",
        options=sidebar_menu_dictionary.keys()
    )

    sidebar.divider()

    sidebar_help_button = sidebar.button(label=":question: Ajuda")
    sidebar_reload_button = sidebar.button(label=":cd: Recarregar")
    sidebar_logoff_button = sidebar.button(label=":lock: Sair")

    if sidebar_help_button:
        Help().main_menu()

    if sidebar_reload_button:
        with sidebar:
            with st.spinner(text="Recarregando..."):
                sleep(1.25)
                st.rerun()

    if sidebar_logoff_button:

        with sidebar:
            logout()

    if sidebar_choice:
        call_interface = sidebar_menu_dictionary[sidebar_choice]
        call_interface.main_menu()

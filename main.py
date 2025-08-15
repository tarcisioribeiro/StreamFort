"""
Arquivo principal da aplicação.
"""
import mysql.connector
import os
import streamlit as st

st.set_page_config(
        page_title="StreamFort - Gerenciador de Senhas",
        page_icon=":closed_lock_with_key:",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
actual_path = os.getcwd()
software_env_path = '{}/.env'.format(actual_path)

if not os.path.isfile(software_env_path):
    pass

if os.path.isfile(software_env_path):

    try:
        from dictionary.sql.user_queries import check_user_query
        from dictionary.vars import to_remove_list
        from functions.query_executor import QueryExecutor

        check_user_quantity = (
            QueryExecutor().simple_consult_query(
                check_user_query,
                ()
            )
        )
        check_user_quantity = (
            QueryExecutor().treat_simple_result(
                check_user_quantity,
                to_remove_list
            )
        )
        check_user_quantity = int(check_user_quantity)

        if check_user_quantity == 0:
            st.session_state.session_id = ''
            from functions.login import CreateUser
            CreateUser().main_menu()

        elif check_user_quantity >= 1:
            from functions.login import Menu
            from source.app import HomePage

            def main():

                if "is_logged_in" not in st.session_state:
                    st.session_state.is_logged_in = False
                if st.session_state.is_logged_in:
                    HomePage()
                else:
                    Menu().main_menu()

            if __name__ == "__main__":
                main()

    except mysql.connector.Error as error:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.error(error)

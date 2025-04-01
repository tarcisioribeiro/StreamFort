"""
Arquivo principal da aplicação.
"""

try:
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
        from time import sleep
        import streamlit as st
        
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='seguranca',
                user='root',
                password='123',
                port=3306
            )
            
            if connection.is_connected():
                with open(software_env_path, 'w') as env_archive:
                    env_archive.write("DB_PORT=3306")
                    env_archive.write("\nDB_HOSTNAME=localhost")
                    env_archive.write("\nDB_USER=root")
                    env_archive.write("\nDB_NAME=seguranca")
                    env_archive.write("\nDB_PASSWORD=123")
                sleep(1)
                st.rerun()

        except mysql.connector.Error as error:
            if error.errno == 1049:
                st.error(body="Erro ao conectar ao MySQL: O banco de dados seguranca não existe. Faça a importação do arquivo de backup/implantação.",)
            elif error.errno == 1045:
                st.error(body="Conexão não realizada. Revise os dados de conexão e tente novamente.",)
            else:
                st.error(body="Erro ao conectar ao MySQL: {} .".format(
                    error
                    ),
                )

    if os.path.isfile(software_env_path):
        
        try:
            from dictionary.sql import check_user_query
            from dictionary.vars import db_config, to_remove_list
            from functions.query_executor import QueryExecutor

            connection = mysql.connector.connect(**db_config)
            
            if connection.is_connected():
                query_executor = QueryExecutor()
                check_user_quantity = query_executor.simple_consult_brute_query(check_user_query)
                check_user_quantity = query_executor.treat_simple_result(check_user_quantity, to_remove_list)
                check_user_quantity = int(check_user_quantity)

                if check_user_quantity == 0:
                    st.session_state.sessao_id = ''
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
                if error.errno == 1049:
                    st.error(body="Erro ao conectar ao MySQL: O banco de dados 'seguranca' não existe. Faça a importação do arquivo de backup/implantação.",)

except KeyError as key_error:
    st.info(key_error)
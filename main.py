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

        col1, col2, col3 = st.columns(3)

        with col2:
            st.error(body="Não foi configurado o ambiente de conexão. Informe a senha do banco de dados.",)
        
        st.divider()

        col4, col5, col6 = st.columns(3)

        with col5:
            with st.expander(label="Dados da conexão", expanded=True):
                db_password = st.text_input(label="Senha do banco de dados", help="Senha do banco de dados MySQL, configurada durante a instalação da aplicação.", type="password")
                confirm_database_informations = st.checkbox(label="Confirmar Dados")

            record_database_informations = st.button(label=":floppy_disk: Gravar informações")

            if confirm_database_informations and record_database_informations:

                with st.spinner(text="Aguarde..."):
                    sleep(3)
                
                try:
                    connection = mysql.connector.connect(
                        host='localhost',
                        database='seguranca',
                        user='root',
                        password=db_password,
                        port=3306
                    )
                    
                    if connection.is_connected():
                        with col6:
                            cl1, cl2 = st.columns(2)
                            with cl2:
                                st.success(body="Conexão bem-sucedida ao banco de dados!",)

                        with open(software_env_path, 'w') as env_archive:
                            env_archive.write("DB_PORT={}".format(3306))
                            env_archive.write("\nDB_HOSTNAME={}".format('localhost'))
                            env_archive.write("\nDB_USER={}".format('root'))
                            env_archive.write("\nDB_NAME=seguranca")
                            env_archive.write("\nDB_PASSWORD={}".format(db_password))
                        sleep(1)
                        if os.name != "nt":
                            os.chmod(software_env_path, 0o600)
                            sleep(1)

                        with col6:
                            cl1, cl2 = st.columns(2)
                            with cl2:
                                st.success(body="Dados gravados com sucesso!",)
                                sleep(5)
                        
                        st.rerun()

                except mysql.connector.Error as error:
                    with col6:
                        cl1, cl2 = st.columns(2)
                        with cl2:
                            if error.errno == 1049:
                                st.error(body="Erro ao conectar ao MySQL: O banco de dados seguranca não existe. Faça a importação do arquivo de backup/implantação.",)
                            elif error.errno == 1045:
                                st.error(body="Conexão não realizada. Revise os dados de conexão e tente novamente.",)
                            else:
                                st.error(body="Erro ao conectar ao MySQL: {} .".format(error),)
            elif record_database_informations and confirm_database_informations == False:
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(2.5)
                    cl1, cl2 = st.columns(2)
                    with cl2:
                        st.warning(body="Você deve confirmar os dados antes de prosseguir.")

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
                    from functions.create_user import CreateUser

                    create_user = CreateUser()
                    create_user.main_menu()

                elif check_user_quantity >= 1:
                    from functions.login import Login
                    from source.app import HomePage

                    def main():

                        if "is_logged_in" not in st.session_state:
                            st.session_state.is_logged_in = False
                        if st.session_state.is_logged_in:
                            HomePage()
                        else:
                            call_user = Login()
                            call_user.get_login()

                    if __name__ == "__main__":
                        main()

        except mysql.connector.Error as error:
            col1, col2, col3 = st.columns(3)
            with col2:
                if error.errno == 1049:
                    st.error(body="Erro ao conectar ao MySQL: O banco de dados 'seguranca' não existe. Faça a importação do arquivo de backup/implantação.",)

except KeyError as key_error:
    st.info(key_error)
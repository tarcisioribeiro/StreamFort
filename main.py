try:

    import mysql.connector
    import os
    import streamlit as st

    st.set_page_config(
            page_title="Gerenciador de Senhas",
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
    session_state_path = '{}/data/session_state.py'.format(actual_path)

    if not os.path.isfile(software_env_path):
        from time import sleep
        import streamlit as st

        col1, col2, col3 = st.columns(3)

        with col2:
            st.error(body="Não foi configurado o ambiente de conexão. Informe os dados de conexão.", icon="🚨")
        
        st.divider()

        col4, col5, col6 = st.columns(3)

        with col5:
            with st.expander(label="Dados da conexão", expanded=True):
                db_port = st.number_input(label="Porta do banco de dados", step=1, value=3306)
                db_hostname = st.text_input(label="Host do banco de dados", placeholder="localhost")
                db_user = st.text_input(label="Usuário do banco de dados", placeholder="root")
                db_password = st.text_input(label="Senha do banco de dados", type="password")
                confirm_database_informations = st.checkbox(label="Confirmar Dados")

            record_database_informations = st.button(label=":floppy_disk: Gravar informações")

            if confirm_database_informations and record_database_informations:

                with st.spinner(text="Aguarde..."):
                    sleep(3)
                
                try:
                    connection = mysql.connector.connect(
                        host=db_hostname,
                        database='seguranca',
                        user=db_user,
                        password=db_password,
                        port=db_port 
                    )
                    
                    if connection.is_connected():
                        with col6:
                            cl1, cl2 = st.columns(2)
                            with cl2:
                                st.success(body="Conexão bem-sucedida ao banco de dados!", icon="✅")

                        with open(software_env_path, 'w') as env_archive:
                            env_archive.write("DB_PORT={}".format(db_port))
                            env_archive.write("\nDB_HOSTNAME={}".format(db_hostname))
                            env_archive.write("\nDB_USER={}".format(db_user))
                            env_archive.write("\nDB_NAME=seguranca")
                            env_archive.write("\nDB_PASSWORD={}".format(db_password))

                        with col6:
                            cl1, cl2 = st.columns(2)
                            with cl2:
                                st.success(body="Dados gravados com sucesso!", icon="✅")
                                sleep(5)
                        
                        st.rerun()

                except mysql.connector.Error as error:
                    with col6:
                        cl1, cl2 = st.columns(2)
                        with cl2:
                            if error.errno == 1049:
                                st.error(body="Erro ao conectar ao MySQL: O banco de dados seguranca não existe. Faça a importação do arquivo de backup/implantação.", icon="🚨")
                            elif error.errno == 1045:
                                st.error(body="Conexão não realizada. Revise os dados de conexão e tente novamente.", icon="🚨")
                            else:
                                st.error(body="Erro ao conectar ao MySQL: {} .".format(error), icon="🚨")


    if not os.path.isfile(session_state_path):

        with open(session_state_path, 'w') as session_state_archive:
            session_state_archive.write("logged_user = ''")
            session_state_archive.write("\nlogged_user_password = ''")

    if os.path.isfile(software_env_path):
        

        try:
            from dictionary.sql import check_user_query
            from dictionary.vars import db_config, to_remove_list
            from functions.query_executor import QueryExecutor

            connection = mysql.connector.connect(**db_config)
            
            if connection.is_connected():
                
                query_executor = QueryExecutor()

                check_user_quantity = query_executor.simple_consult_query(check_user_query)
                check_user_quantity = query_executor.treat_simple_result(check_user_quantity, to_remove_list)
                check_user_quantity = int(check_user_quantity)

                if check_user_quantity == 0:
                    from functions.create_user import CreateUser

                    create_user = CreateUser()
                    create_user.main_menu()

                elif check_user_quantity >= 1:

                    from functions.login import User
                    from source.app import HomePage

                    def main():

                        if "is_logged_in" not in st.session_state:
                            st.session_state.is_logged_in = False

                        if st.session_state.is_logged_in:
                            HomePage()
                        else:
                            call_user = User()
                            call_user.get_login()


                    if __name__ == "__main__":
                        main()

        except mysql.connector.Error as error:
            col1, col2, col3 = st.columns(3)
            with col2:
                if error.errno == 1049:
                    st.error(body="Erro ao conectar ao MySQL: O banco de dados seguranca não existe. Faça a importação do arquivo de backup/implantação.", icon="🚨")

except KeyError:
    st.rerun()
import streamlit as st
import mysql.connector
from dictionary.sql import name_query, sex_query
from dictionary.vars import absolute_app_path, db_config, to_remove_list
from functions.query_executor import QueryExecutor
from time import sleep


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


class User:
    def __init__(self):

        query_executor = QueryExecutor()

        def check_login(user, password):
            query = "SELECT * FROM usuarios WHERE login = %s AND senha = %s"
            cursor.execute(query, (user, password))
            return cursor.fetchone() is not None
        
        def check_user():
            name = query_executor.simple_consult_query(name_query)
            name = query_executor.treat_simple_result(name, to_remove_list)

            sex = query_executor.simple_consult_query(sex_query)
            sex = query_executor.treat_simple_result(sex, to_remove_list)

            return name, sex
        
        def show_user(name, sex):
            if sex == "M":
                st.image(image="{}/library/images/man.png".format(absolute_app_path))
            elif sex == "F":
                st.image(image="{}/library/images/woman.png".format(absolute_app_path))
            st.text(body="{}".format(name))
            st.divider()

        def get_login():

            col1, col2, col3 = st.columns(3)

            with col2:

                st.header(body=":key: StreamFort")

                with st.container():
                    with st.expander(label=":computer: Login", expanded=True):

                        user = st.text_input(":closed_lock_with_key: Usuário")
                        password = st.text_input(":key: Senha", type="password")
                        login_button = st.button(label=":unlock: Entrar")

                        if login_button:
                            if check_login(user, password):
                                with st.spinner("Aguarde..."):
                                    sleep(1)
                                    st.toast("Login bem-sucedido!")

                                    log_query = '''INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES (%s, %s, %s)'''
                                    log_values = (user, 'Acesso', 'O usuário acessou o sistema.')
                                    query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

                                    with open("data/session_state.py", "w") as arquivo:
                                        arquivo.write("logged_user = '{}'\n".format(user))
                                        arquivo.write(
                                            "logged_user_password = '{}'\n".format(password)
                                        )
                                    sleep(1)

                                st.session_state.is_logged_in = True
                                st.rerun()

                            else:
                                st.error("Login falhou. Verifique suas credenciais.")

        self.get_login = get_login
        self.check_user = check_user
        self.show_user = show_user

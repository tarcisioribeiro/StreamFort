from data.session_state import logged_user
from dictionary.sql import check_user_query
from dictionary.vars import to_remove_list
from functions.query_executor import QueryExecutor
from functions.validate_document import Documents
from functions.variables import Variables
from time import sleep
import streamlit as st
import bcrypt


class CreateUser:

    def __init__(self):

        query_executor = QueryExecutor()
        document = Documents()

        def hash_password(password: str) -> bytes:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt)

        def is_login_valid(login: str):
            has_upper = any(c.isupper() for c in login)
            has_digit = any(c.isdigit() for c in login)
            has_special = any(not c.isalnum() for c in login)
            if " " in login or has_upper or has_digit or has_special:
                st.error(body="O Login '{}' é inválido.".format(login))
                return False
            else:
                st.success(body="O login '{}' é válido.".format(login))
                return True
            
        def is_password_valid(password: str):
            has_upper = any(c.isupper() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(not c.isalnum() for c in password)
            if " " in password or has_upper == False or has_digit == False or has_special == False or len(password) < 8:
                st.error(body="A senha informada é inválida.".format(password))
                return False
            else:
                st.success(body="A senha informada é válida.".format(password))
                return True

        def main_menu():

            check_user_quantity = query_executor.simple_consult_query(check_user_query)
            check_user_quantity = query_executor.treat_simple_result(check_user_quantity, to_remove_list)
            check_user_quantity = int(check_user_quantity)

            if check_user_quantity == 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.header(body=":floppy_disk: Cadastro de usuário")
                st.divider()

            col4, col5, col6 = st.columns(3)

            if check_user_quantity == 0:

                with col6:
                    cl1, cl2 = st.columns(2)
                    with cl2:
                        st.warning(body="Nenhum usuário cadastrado. Cadastre o primeiro usuário.")

            with col4:
                with st.expander(label="Dados de login", expanded=True):
                    user_login = st.text_input(label="Login de usuário",max_chars=25,help="O login deve conter apenas letras minúsculas, sem espaços.",)
                    user_password = st.text_input(label="Senha de usuário",max_chars=100,help="A senha deve conter ao mínimo 8 caracteres, 1 letra maiúscula, 1 minúscula e 1 caractere especial, sem espaços.",type="password", key="user_password")
                    confirm_user_password = st.text_input(label="Confirmação de senha",max_chars=100,help="Deve ser a mesma informada no campo acima.",type="password", key="confirm_user_password")

                confirm_values = st.checkbox(label="Confirmar dados")

            sex_options = {"Masculino": "M", "Feminino": "F"}
            
            with col5:
                with st.expander(label="Dados do usuário", expanded=True):
                    user_name = st.text_input(label="Nome de usuário",max_chars=100,help="Informe aqui seu nome completo.",)
                    user_document = st.text_input(label="Documento do usuário", help="Informe seu CPF neste campo.")
                    user_sex = st.selectbox(label="Sexo do usuário", options=sex_options.keys())

                insert_new_user_button = st.button(label=":floppy_disk: Cadastrar novo usuário")

                if insert_new_user_button:
                    user_sex = sex_options[user_sex]
                    if confirm_values == True:
                        with st.spinner(text="Aguarde..."):
                            sleep(2)
                        with col6:
                            cl1, cl2 = st.columns(2)
                            with cl2:
                                is_document_valid = document.validate_owner_document(user_document)
                                valid_login = is_login_valid(user_login)
                                valid_password = is_password_valid(user_password)

                        if user_login != "" and user_password != "" and confirm_user_password != "" and (user_password == confirm_user_password) and user_name != "" and is_document_valid == True and valid_login == True and valid_password == True:

                            hashed_password = hash_password(user_password)

                            if check_user_quantity == 0:
                                insert_new_user_query = """INSERT INTO usuarios (login, senha, nome, documento_usuario, sexo) VALUES (%s, %s, %s, %s, %s)"""
                                new_user_values = (user_login,hashed_password,user_name,user_document,user_sex)
                                query_executor.insert_query(insert_new_user_query,new_user_values,"Novo usuário cadastrado com sucesso!","Erro ao cadastrar novo usuário:")

                                log_query = '''INSERT INTO seguranca.logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES ( %s, %s, %s);'''
                                log_values = (user_login, "Registro", "O usuário foi cadastrado no sistema.")
                                query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

                                with st.spinner(text="Recarregando..."):
                                    sleep(5)
                                    st.rerun()

                            elif check_user_quantity >= 1:

                                with col6:
                                    cl1, cl2 = st.columns(2)
                                    with cl2:
                                        check_if_user_document_exists_query = """SELECT COUNT(id_usuario) FROM usuarios WHERE cpf = {};""".format(user_document)
                                        check_if_user_exists = query_executor.simple_consult_query(check_if_user_document_exists_query)
                                        check_if_user_exists = query_executor.treat_simple_result(check_if_user_exists, to_remove_list)
                                        check_if_user_exists = int(check_if_user_exists)

                                        if check_if_user_exists == 0:
                                            insert_new_user_query = """INSERT INTO usuarios (login, senha, nome, cpf, sexo) VALUES (%s, %s, %s, %s, %s)"""
                                            new_user_values = (user_login,hashed_password,user_name,user_document,user_sex)
                                            query_executor.insert_query(insert_new_user_query,new_user_values,"Novo usuário cadastrado com sucesso!","Erro ao cadastrar novo usuário:")

                                            log_query = '''INSERT INTO seguranca.logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES ( %s, %s, %s);'''
                                            log_values = (logged_user, "Registro", "Cadastrou o usuário {} associado ao documento {} no sistema.".format(user_name, user_document))
                                            query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

                                            sleep(2)
                                        elif check_if_user_exists >= 1:
                                            st.error(
                                                "Já existe um usuário cadastrado associado ao documento {}.".format(user_document)
                                            )

                        elif user_login == "" or user_password == "" or user_name == "" or is_document_valid == False or valid_login == False or valid_password == False or confirm_user_password == "" or (user_password != confirm_user_password):
                            with cl2:
                                if user_login == "":
                                    st.error("O login não foi preenchido.")
                                if user_password == "":
                                    st.error("A senha não foi preenchida.")
                                if user_name == "":
                                    st.error("O nome não foi preenchido.")
                                if confirm_user_password == "":
                                    st.error("A confirmação da senha não foi preenchida.")
                                if user_password != confirm_user_password and (user_password != "" and confirm_user_password != ""):
                                    st.error("As senhas não correspondem.")

                    elif confirm_values == False:
                        st.warning(body=":warning: Revise os dados e confirme-os antes de prosseguir.")

        self.main_menu = main_menu
from data.session_state import logged_user
from data.user_data import logged_user_name, logged_user_document
from dictionary.vars import field_names, to_remove_list
from dictionary.sql import search_accounts_query, check_user_passwords_quantity_query
from functions.query_executor import QueryExecutor
from time import sleep
import streamlit as st


class Passwords:

    def __init__(self) -> None:

        query_executor = QueryExecutor()
        
        def get_new_password():

            col1, col2, col3 = st.columns(3)

            with col2:

                with st.expander(label="Dados", expanded=True):

                    site = st.text_input(label='Nome Site')
                    url = st.text_input(label='URL do Site')
                    name = st.text_input(label='Nome')
                    login = st.text_input(label='Login')
                    password = st.text_input(label="Senha", type="password")
                    comment = st.text_input(label="Comentário")

                send_button = st.button(':floppy_disk: Cadastrar Senha')

                if send_button:

                    with st.spinner(text="Aguarde..."):
                        sleep(1.5)

                    insert_password_query = "INSERT INTO senhas(nome_site, url_site, nome, login, senha, comentario, usuario_associado, documento_usuario_associado) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                    query_values = (site, url, name, login, password, comment, logged_user_name, logged_user_document)

                    query_executor.insert_query(query=insert_password_query, values=query_values, success_message='Senha cadastrada com sucesso!', error_message='Erro ao cadastrar senha:')

                    log_query = '''INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                    log_query_values = (logged_user, 'Cadastro', 'Cadastrou a senha {} associada ao email {}'.format(query_values[0], query_values[3]))
                    query_executor.insert_query(query=log_query, values=log_query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

        def show_account():

            user_passwords_quantity = query_executor.simple_consult_query(check_user_passwords_quantity_query)
            user_passwords_quantity = query_executor.treat_simple_result(user_passwords_quantity, to_remove_list)
            user_passwords_quantity = int(user_passwords_quantity)

            col1, col2, col3 = st.columns(3)

            if user_passwords_quantity == 0:
                with col2:
                    st.warning(body="Você ainda não possui senhas cadastradas.", icon="⚠️")

            elif user_passwords_quantity >= 1:

                with col3:

                    cl1, cl2 = st.columns(2)

                    user_accounts = ["Selecione uma opção"]

                    accounts = query_executor.complex_consult_query(query=search_accounts_query)
                    accounts = query_executor.treat_numerous_simple_result(accounts, to_remove_list)

                    for i in range(0, len(accounts)):
                        user_accounts.append(accounts[i])

                    with col1:

                        cl1, cl2 = st.columns(2)

                        with cl1:

                            selected_option = st.selectbox(label="Selecione a conta", options=user_accounts)

                            consult_button = st.button(label=":floppy_disk: Consultar senha")

                    account_details_query = '''SELECT senhas.nome_site, senhas.url_site, senhas.login, senhas.senha FROM senhas WHERE senhas.nome_site = '{}' AND senhas.usuario_associado = '{}' AND senhas.documento_usuario_associado = '{}';'''.format(selected_option, logged_user_name, logged_user_document)

                    result_list = query_executor.complex_consult_query(query=account_details_query)
                    result_list = query_executor.treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

                    if selected_option != "Selecione uma opção" and consult_button:

                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(1.5)

                            with st.expander(label="Dados", expanded=True):

                                aux_string = ''

                                for i in range(0, len(result_list)):
                                    if i == len(result_list) - 1:
                                        st.write(field_names[i])
                                        st.code(body="{}".format(result_list[i]))
                                    else:
                                        st.write(field_names[i])
                                        aux_string = str(result_list[i])
                                        aux_string = aux_string.replace('"', '')
                                        st.code(body="{}".format(aux_string))

                                log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                                query_values = (logged_user, 'Consulta', 'Consultou a senha {} associada ao email {}'.format(result_list[0], result_list[2]))
                                query_executor.insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')


        def show_passwords_interface():

            col1, col2, col3 = st.columns(3)

            with col2:
                password_option = st.selectbox(label="Opções", options=["Cadastrar Senha", "Consultar Senha"])
            
            st.divider()

            if password_option == 'Consultar Senha':
                show_account()

            elif password_option == 'Cadastrar Senha':
                get_new_password()

        self.interface = show_passwords_interface
from dictionary.vars import field_names, to_remove_list
from dictionary.sql import search_accounts_query, check_user_passwords_quantity_query
from functions.query_executor import QueryExecutor
from functions.login import Login
from time import sleep
import streamlit as st


class Passwords:
    """
    Classe que representa as senhas, com as quatro funções básicas de um CRUD.
    """
    def check_if_account_name_already_exists(self, account: str):
        """
        Verifica se o nome da conta já foi utilizado anteriormente.

        Returns
        -------
        is_account_name_available : bool
            Se o nome de conta está disponível ou não.
        """
        logged_user_name, logged_user_document = Login().get_user_data(return_option="user_login_password")

        is_account_name_available: bool

        accounts_with_parameter_name_query = """SELECT COUNT(id_senha) FROM senhas WHERE nome_site = %s AND usuario_associado = %s AND documento_usuario_associado = %s;"""
        query_values = (account, logged_user_name, logged_user_document)
        accounts_with_parameter_name_quantity = QueryExecutor().simple_consult_query(query=accounts_with_parameter_name_query, params=query_values)
        accounts_with_parameter_name_quantity = QueryExecutor().treat_simple_result(value_to_treat=accounts_with_parameter_name_quantity, values_to_remove=to_remove_list)
        accounts_with_parameter_name_quantity = int(
            accounts_with_parameter_name_quantity)

        if accounts_with_parameter_name_quantity == 0:
            is_account_name_available = True
        else:
            is_account_name_available = False

        return is_account_name_available

    def get_user_passwords_quantity(self):
        """
        Consulta a quantidade de senhas cadastradas pelo usuário.

        Returns
        -------
        user_passwords_quantity : int
            A quantidade de senhas cadastradas pelo usuário.
        """
        logged_user, logged_user_password = Login().get_user_data(return_option="user_login_password")

        user_passwords_quantity = QueryExecutor().simple_consult_query(check_user_passwords_quantity_query, params=(logged_user, logged_user_password))
        user_passwords_quantity = QueryExecutor().treat_simple_result(user_passwords_quantity, to_remove_list)
        user_passwords_quantity = int(user_passwords_quantity)

        return user_passwords_quantity

    def get_user_accounts_names(self):
        """
        Consulta o nome das contas cadastradas pelo usuário.

        Returns
        -------
        user_accounts : list
            Lista com os nomes das contas do usuário.
        """
        logged_user, logged_user_password = Login().get_user_data(return_option="user_login_password")

        user_accounts = []

        accounts = QueryExecutor().complex_consult_query(query=search_accounts_query, params=(logged_user, logged_user_password))
        accounts = QueryExecutor().treat_numerous_simple_result(accounts, to_remove_list)

        for i in range(0, len(accounts)):
            user_accounts.append(accounts[i])

        return user_accounts

    def create_new_password(self):
        """
        Função para criação de uma nova senha.
        """
        logged_user_name, logged_user_document = Login().get_user_data(return_option="user_doc_name")
        logged_user, logged_user_password = Login().get_user_data(return_option="user_login_password")

        col1, col2 = st.columns(2)
        with col2:
            data_validator_expander = st.expander(label="Validação dos dados", expanded=True)

        with col1:

            with st.expander(label="Dados", expanded=True):

                site = st.text_input(label='Nome Site',)
                url = st.text_input(label='URL/Link do Site')
                login = st.text_input(label='Login', help="Seu usuário no site")
                password = st.text_input(label="Senha", type="password", help="Sua senha do site")
                confirm_values = st.checkbox(label="Confirmar dados", value=False)

            send_button = st.button(':floppy_disk: Cadastrar Senha')

            if send_button and confirm_values == True:
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(2.5)
                if site != '' and url != '' and login != '' and password != '':
                    is_name_available = self.check_if_account_name_already_exists(account=site)
                    if is_name_available:
                        with col2:
                            with data_validator_expander:
                                st.success(body="Nome de conta válida.")
                        insert_password_query = "INSERT INTO senhas(nome_site, url_site, login, senha, usuario_associado, documento_usuario_associado) VALUES(%s, %s, %s, %s, %s, %s)"
                        query_values = (site, url, login, password, logged_user_name, logged_user_document)
                        QueryExecutor().insert_query(query=insert_password_query, values=query_values,success_message='Senha cadastrada com sucesso!', error_message='Erro ao cadastrar senha:')
                        log_query = '''INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                        log_query_values = (logged_user, 'Cadastro', 'Cadastrou a senha {} associada ao email {}'.format(query_values[0], query_values[3]))
                        QueryExecutor().insert_query(query=log_query, values=log_query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')
                    else:
                        with col2:
                            with data_validator_expander:
                                st.error(body="O nome da conta já está sendo utilizado.")
                else:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error('Há um ou mais campos vazios.')

            elif send_button and confirm_values == False:
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(0.5)
                    with data_validator_expander:
                        st.warning(body="Você deve confirmar os dados antes de prosseguir.")

    def read_password(self):
        """
        Função para a consulta de uma senha.
        """
        logged_user_name, logged_user_document = Login().get_user_data(return_option="user_doc_name")
        logged_user, logged_user_password = Login().get_user_data(return_option="user_login_password")

        user_passwords_quantity = self.get_user_passwords_quantity()

        if user_passwords_quantity == 0:
            col1, col2, col3 = st.columns(3)

            with col2:
                st.warning(body="Você ainda não possui senhas cadastradas.")

        elif user_passwords_quantity >= 1:
            col1, col2 = st.columns(2)
            user_accounts = self.get_user_accounts_names()

            with col2:
                data_validator_expander = st.expander(
                    label="Validação dos dados", expanded=True)

            with col1:
                with st.expander(label="Consulta", expanded=True):
                    selected_option = st.selectbox(label="Selecione a conta", options=user_accounts)
                    safe_password = st.text_input(label="Informe sua senha", type="password", help="Corresponde a senha utilizada para acessar a aplicação.")
                    confirm_safe_password = st.text_input(label="Confirme sua senha", type="password", help="Deve ser idêntica a senha informada acima.")
                    confirm_selection = st.checkbox(label="Confirmar seleção")

                consult_button = st.button(label=":file_folder: Consultar senha")

            account_details_query = '''
                SELECT 
                    senhas.nome_site,
                    senhas.url_site,
                    senhas.login,
                    senhas.senha
                FROM
                    senhas
                WHERE
                    senhas.nome_site = %s
                        AND senhas.usuario_associado = %s
                        AND senhas.documento_usuario_associado = %s;
            '''
            account_details_values = (selected_option, logged_user_name, logged_user_document)

            result_list = QueryExecutor().complex_consult_query(query=account_details_query, params=account_details_values)
            result_list = QueryExecutor().treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

            if confirm_selection and consult_button:
                is_password_valid, hashed_password = Login().check_login(logged_user, safe_password)
                if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)
                        with st.expander(label="Dados", expanded=True):
                            aux_string = ''
                            for i in range(0, len(result_list)):
                                st.write(field_names[i])
                                aux_string = str(result_list[i])
                                if aux_string.startswith('b'):
                                    aux_string = aux_string[1:]
                                st.code(body="{}".format(aux_string))

                            log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                            query_values = (logged_user, 'Consulta', 'Consultou a senha do site {}'.format(selected_option))
                            QueryExecutor().insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

                elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error(body="A senha informada é inválida.")

                elif safe_password != confirm_safe_password and (safe_password != "" and confirm_safe_password != ""):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error(body="As senhas informadas não coincidem.")

                elif safe_password == '' or confirm_safe_password == '':
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            if safe_password == '':
                                st.error(body="A senha não foi preenchida.")
                            if confirm_safe_password == '':
                                st.error(body="A confirmação da senha não foi preenchida.")

            elif confirm_selection == False and consult_button:
                with col3:
                    with st.spinner(text="Aguarde..."):
                        sleep(0.5)
                    with data_validator_expander:
                        st.warning(body="Confirme a seleção antes de realizar a consulta.")

    def update_password(self):
        """
        Função para a atualização de uma senha.
        """
        logged_user_name, logged_user_document = Login().get_user_data(return_option="user_login_password")
        logged_user, logged_user_password = Login().get_user_data(return_option="user_doc_name")

        user_passwords_quantity = self.get_user_passwords_quantity()

        if user_passwords_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui senhas cadastradas.")

        elif user_passwords_quantity >= 1:
            col1, col2 = st.columns(2)
            user_accounts = self.get_user_accounts_names()

            with col2:
                data_validator_expander = st.expander(
                    label="Validação dos dados", expanded=True)

            with col1:
                with st.expander(label="Consulta", expanded=True):
                    selected_option = st.selectbox(
                        label="Selecione a conta", options=user_accounts)
                    safe_password = st.text_input(
                        label="Informe sua senha", type="password", help="Corresponde a senha utilizada para acessar a aplicação.")
                    confirm_safe_password = st.text_input(label="Confirme sua senha", type="password", help="Deve ser idêntica a senha informada acima.")
                    confirm_selection = st.checkbox(label="Confirmar seleção")

            account_details_query = '''
                SELECT 
                    senhas.nome_site,
                    senhas.url_site,
                    senhas.login,
                    senhas.senha
                FROM
                    senhas
                WHERE
                    senhas.nome_site = %s
                        AND senhas.usuario_associado = %s
                        AND senhas.documento_usuario_associado = %s;
            '''
            account_details_values = (selected_option, logged_user_name, logged_user_document)

            result_list = QueryExecutor().complex_consult_query(query=account_details_query, params=account_details_values)
            result_list = QueryExecutor().treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

            if confirm_selection:
                is_password_valid, hashed_password = Login().check_login(logged_user, safe_password)
                if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with st.expander(label="Novos dados", expanded=True):
                            st.info(body="Site: {}".format(selected_option))
                            url = st.text_input(label='URL/Link do Site')
                            login = st.text_input(label='Login', help="Seu usuário no site")
                            password = st.text_input(label="Senha", type="password", help="Sua senha do site")
                            confirm_values = st.checkbox(label="Confirmar dados", value=False)

                        send_button = st.button(':arrows_counterclockwise: Atualizar Senha')

                        if confirm_values and send_button:
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(2.5)
                            update_site_query = '''UPDATE senhas SET url_site = %s, login = %s, senha = %s WHERE nome_site = %s AND usuario_associado = %s AND documento_usuario_associado = %s;'''
                            update_site_values = (url, login, password, selected_option, logged_user_name, logged_user_document)
                            QueryExecutor().insert_query(query=update_site_query, values=update_site_values, success_message="Senha atualizada com sucesso!", error_message="Erro ao atualizar senha:")
                            log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                            query_values = (logged_user, 'Atualização', 'Atualizou a senha do site {}.'.format(selected_option))
                            QueryExecutor().insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

                if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error(body="A senha informada é inválida.")

                elif safe_password != "" and confirm_safe_password != "" and safe_password != confirm_safe_password:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error(body="As senhas informadas não coincidem.")

    def delete_password(self):
        """
        Função para a exclusão de uma senha.
        """
        logged_user_name, logged_user_document = Login().get_user_data(return_option="user_login_password")
        logged_user, logged_user_password = Login().get_user_data(return_option="user_doc_name")

        user_passwords_quantity = self.get_user_passwords_quantity()

        if user_passwords_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui senhas cadastradas.")
        elif user_passwords_quantity >= 1:
            col1, col2 = st.columns(2)
            user_accounts = self.get_user_accounts_names()
            data_validator_expander = st.expander(label="Validação dos dados", expanded=True)
            with col1:
                with st.expander(label="Consulta", expanded=True):
                    selected_option = st.selectbox(label="Selecione a conta", options=user_accounts)
                    safe_password = st.text_input(label="Informe sua senha", type="password", help="Corresponde a senha utilizada para acessar a aplicação.")
                    confirm_safe_password = st.text_input(label="Confirme sua senha", type="password", help="Deve ser idêntica a senha informada acima.")
                    confirm_selection = st.checkbox(label="Confirmar seleção")

            account_details_query = '''
                SELECT 
                    senhas.nome_site,
                    senhas.url_site,
                    senhas.login,
                    senhas.senha
                FROM
                    senhas
                WHERE
                    senhas.nome_site = %s
                        AND senhas.usuario_associado = %s
                        AND senhas.documento_usuario_associado = %s;
            '''
            account_details_values = (selected_option, logged_user_name, logged_user_document)
            result_list = QueryExecutor().complex_consult_query(query=account_details_query, params=account_details_values)
            result_list = QueryExecutor().treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

            if confirm_selection:
                is_password_valid, hashed_password = Login().check_login(logged_user, safe_password)
                if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:

                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with st.expander(label="Dados", expanded=True):
                            aux_string = ''
                            for i in range(0, len(result_list)):
                                st.write(field_names[i])
                                aux_string = str(result_list[i])
                                if aux_string.startswith('b'):
                                    aux_string = aux_string[1:]
                                st.code(body="{}".format(aux_string))
                            confirm_delete_selection = st.checkbox(label="Confirmar exclusão")
                        delete_password_button = st.button(label=":wastebasket: Deletar senha")

                    if confirm_delete_selection and delete_password_button:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(2.5)

                            delete_password_query = '''DELETE senhas FROM senhas WHERE nome_site = %s AND usuario_associado = %s AND documento_usuario_associado = %s;'''
                            delete_password_values = (selected_option, logged_user_name, logged_user_document)
                            QueryExecutor().insert_query(query=delete_password_query, values=delete_password_values, success_message="Senha excluída com sucesso!", error_message="Erro ao excluir senha:")

                            log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                            query_values = (logged_user, 'Exclusão', 'Excluiu a senha do site {}'.format(selected_option))
                            QueryExecutor().insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

                    elif confirm_delete_selection == False and delete_password_button:
                        with col1:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            with data_validator_expander:
                                st.warning(body="Confirme a exclusão da senha.")

                elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error(body="A senha informada é inválida.")

                elif safe_password != confirm_safe_password:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        with data_validator_expander:
                            st.error(body="As senhas informadas não coincidem.")

    def main_menu(self):
        """
        Menu Principal.
        """
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header(body=":lock: Senhas")

        with col2:
            menu_options = ["Cadastrar senha", "Consultar senha", "Atualizar senha", "Deletar senha"]
            password_option = st.selectbox(label="Menu", options=menu_options)

        st.divider()

        if password_option == menu_options[0]:
            self.create_new_password()
        elif password_option == menu_options[1]:
            self.read_password()
        elif password_option == menu_options[2]:
            self.update_password()
        elif password_option == menu_options[3]:
            self.delete_password()

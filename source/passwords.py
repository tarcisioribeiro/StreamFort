from dictionary.user_data import user_id, user_document
from dictionary.vars import field_names, to_remove_list
from dictionary.sql.other_queries import log_query
from dictionary.sql.password_queries import (
    account_details_query,
    accounts_with_parameter_name_query,
    check_user_passwords_quantity_query,
    delete_password_query,
    insert_password_query,
    search_accounts_query,
    update_site_query
)
from functions.query_executor import QueryExecutor
from functions.login import Login
from time import sleep
import streamlit as st


class Passwords:
    """
    Classe que representa as senhas, com as quatro funções básicas de um CRUD.
    """

    def check_if_account_name_already_exists(
            self,
            account: str
    ):
        """
        Verifica se o nome da conta já foi utilizado anteriormente.

        Returns
        -------
        is_account_name_available : bool
            Se o nome de conta está disponível ou não.
        """

        is_account_name_available: bool

        query_values = (account, user_id, user_document)
        accounts_with_name_quantity = QueryExecutor().simple_consult_query(
            query=accounts_with_parameter_name_query,
            params=query_values
        )
        accounts_with_name_quantity = QueryExecutor().treat_simple_result(
            value_to_treat=accounts_with_name_quantity,
            values_to_remove=to_remove_list
        )
        accounts_with_parameter_name_quantity = int(
            accounts_with_name_quantity
        )

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

        user_passwords_quantity = QueryExecutor().simple_consult_query(
            check_user_passwords_quantity_query,
            params=(user_id, user_document)
        )
        user_passwords_quantity = QueryExecutor().treat_simple_result(
            user_passwords_quantity,
            to_remove_list
        )
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

        user_accounts = []

        accounts = QueryExecutor().complex_consult_query(
            query=search_accounts_query,
            params=(user_id, user_document)
        )
        accounts = QueryExecutor().treat_simple_results(
            accounts,
            to_remove_list
        )

        for i in range(0, len(accounts)):
            user_accounts.append(accounts[i])

        return user_accounts

    def create_new_password(self):
        """
        Função para criação de uma nova senha.
        """

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(body=":computer: Entrada de Dados")
            with st.expander(label="Dados", expanded=True):

                site = st.text_input(label='Nome Site',)
                url = st.text_input(label='URL/Link do Site')
                login = st.text_input(
                    label='Login',
                    help="Seu usuário no site"
                )
                password = st.text_input(
                    label="Senha",
                    type="password",
                    help="Sua senha do site"
                )
                confirm_values = st.checkbox(
                    label="Confirmar dados",
                    value=False
                )

            send_button = st.button(':floppy_disk: Cadastrar Senha')

            if send_button and confirm_values:
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(1.25)
                if site != '' and url != '' and login != '' and password != '':
                    is_available = self.check_if_account_name_already_exists(
                        account=site
                    )
                    if is_available:
                        with col2:
                            st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.success(body="Nome de conta válida.")

                        query_values = (
                            site,
                            url,
                            login,
                            password,
                            user_id,
                            user_document
                        )
                        QueryExecutor().insert_query(
                            query=insert_password_query,
                            values=query_values,
                            success_message='Senha cadastrada com sucesso!',
                            error_message='Erro ao cadastrar senha:'
                        )

                        log_query_values = (
                            user_id,
                            'Cadastro',
                            'Cadastrou a senha {} no email {}'.format(
                                query_values[0],
                                query_values[3]
                            )
                        )
                        QueryExecutor().insert_query(
                            query=log_query,
                            values=log_query_values,
                            success_message='Log gravado.',
                            error_message='Erro ao gravar log:'
                        )
                    else:
                        with col2:
                            st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(body="Este nome já está sendo usado.")
                else:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error('Há um ou mais campos vazios.')

            elif send_button and confirm_values:
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(0.5)
                    st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                    with st.expander(
                        label="Validação dos dados",
                        expanded=True
                    ):
                        st.warning(body="Confirme os dados para prosseguir.")

    def read_password(self):
        """
        Função para a consulta de uma senha.
        """

        user_passwords_quantity = self.get_user_passwords_quantity()

        if user_passwords_quantity == 0:
            col1, col2, col3 = st.columns(3)

            with col2:
                st.warning(body="Você ainda não possui senhas cadastradas.")

        elif user_passwords_quantity >= 1:
            col1, col2 = st.columns(2)
            user_accounts = self.get_user_accounts_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_option = st.selectbox(
                        label="Selecione a conta",
                        options=user_accounts
                    )
                    safe_password = st.text_input(
                        label="Informe sua senha",
                        type="password",
                        help="Corresponde a senha para acessar a aplicação."
                    )
                    confirm_safe_password = st.text_input(
                        label="Confirme sua senha",
                        type="password",
                        help="Deve ser idêntica a senha informada acima."
                    )
                    confirm_selection = st.checkbox(label="Confirmar seleção")

                consult_button = st.button(
                    label=":file_folder: Consultar senha"
                )

            account_details_values = (
                selected_option,
                user_id,
                user_document
            )

            result_list = QueryExecutor().complex_consult_query(
                query=account_details_query,
                params=account_details_values
            )
            result_list = QueryExecutor().treat_complex_result(
                values_to_treat=result_list,
                values_to_remove=to_remove_list
            )

            if confirm_selection and consult_button:
                is_password_valid, hashed_password = Login().check_login(
                    user_id,
                    safe_password
                )
                if (
                    safe_password != ""
                    and confirm_safe_password != ""
                    and safe_password == confirm_safe_password
                    and is_password_valid
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(1.25)
                        st.subheader(
                            body=":white_check_mark: Validação da Consulta"
                        )
                        with st.expander(label="Dados", expanded=True):
                            aux_string = ''
                            for i in range(0, len(result_list)):
                                st.write(field_names[i])
                                aux_string = str(result_list[i])
                                if aux_string.startswith('b'):
                                    aux_string = aux_string[1:]
                                st.code(body="{}".format(aux_string))

                            query_values = (
                                user_id,
                                'Consulta',
                                'Consultou a senha do site {}'.format(
                                    selected_option
                                )
                            )
                            QueryExecutor().insert_query(
                                query=log_query,
                                values=query_values,
                                success_message='Log gravado.',
                                error_message='Erro ao gravar log:'
                            )

                elif (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password == confirm_safe_password
                        and is_password_valid
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(body="A senha informada é inválida.")
                elif (
                        safe_password != confirm_safe_password
                        and safe_password != ""
                        and confirm_safe_password != ""
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(
                                body="As senhas informadas não coincidem."
                            )

                elif safe_password == '' or confirm_safe_password == '':
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            if safe_password == '':
                                st.error(body="A senha não foi preenchida.")
                            if confirm_safe_password == '':
                                st.error(
                                    body="A confirmação não foi preenchida."
                                )

            elif (
                    confirm_selection is False
                    and consult_button
            ):
                with col3:
                    with st.spinner(text="Aguarde..."):
                        sleep(0.5)
                    st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                    with st.expander(
                        label="Validação dos dados",
                        expanded=True
                    ):
                        st.warning(
                            body="Confirme a seleção para realizar a consulta."
                        )

    def update_password(self):
        """
        Função para a atualização de uma senha.
        """

        user_passwords_quantity = self.get_user_passwords_quantity()

        if user_passwords_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui senhas cadastradas.")

        elif user_passwords_quantity >= 1:
            col1, col2 = st.columns(2)
            user_accounts = self.get_user_accounts_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_option = st.selectbox(
                        label="Selecione a conta", options=user_accounts)
                    safe_password = st.text_input(
                        label="Informe sua senha",
                        type="password",
                        help="Corresponde a senha para acessar a aplicação."
                    )
                    confirm_safe_password = st.text_input(
                        label="Confirme sua senha",
                        type="password",
                        help="Deve ser idêntica a senha informada acima."
                    )
                    confirm_selection = st.checkbox(label="Confirmar seleção")

            account_details_values = (
                selected_option,
                user_id,
                user_document
            )

            result_list = QueryExecutor().complex_consult_query(
                query=account_details_query,
                params=account_details_values
            )
            result_list = QueryExecutor().treat_complex_result(
                values_to_treat=result_list,
                values_to_remove=to_remove_list
            )

            if confirm_selection:
                is_password_valid, hashed_password = Login().check_login(
                    user_id,
                    safe_password
                )
                if (
                    safe_password != ""
                    and confirm_safe_password != ""
                    and safe_password == confirm_safe_password
                    and is_password_valid
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                            body=":white_check_mark: Dados atualizados"
                        )
                        with st.expander(label="Novos dados", expanded=True):
                            st.info(body="Site: {}".format(selected_option))
                            url = st.text_input(label='URL/Link do Site')
                            login = st.text_input(
                                label='Login',
                                help="Seu usuário no site"
                            )
                            password = st.text_input(
                                label="Senha",
                                type="password",
                                help="Sua senha do site"
                            )
                            confirm_values = st.checkbox(
                                label="Confirmar dados",
                                value=False
                            )

                        send_button = st.button(
                            ':arrows_counterclockwise: Atualizar Senha'
                        )

                        if confirm_values and send_button:
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(1.25)

                            update_site_values = (
                                url,
                                login,
                                password,
                                selected_option,
                                user_id,
                                user_document
                            )
                            QueryExecutor().insert_query(
                                query=update_site_query,
                                values=update_site_values,
                                success_message="Senha atualizada.",
                                error_message="Erro ao atualizar senha:"
                            )

                            query_values = (
                                user_id,
                                'Atualização',
                                'Atualizou a senha do site {}.'.format(
                                    selected_option
                                )
                            )
                            QueryExecutor().insert_query(
                                query=log_query,
                                values=query_values,
                                success_message='Log gravado.',
                                error_message='Erro ao gravar log:'
                            )
                elif (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password != confirm_safe_password
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(body="As senhas não coincidem.")
                elif is_password_valid is False:
                    with col2:
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(body="Senha inválida.")

    def delete_password(self):
        """
        Função para a exclusão de uma senha.
        """

        user_passwords_quantity = self.get_user_passwords_quantity()

        if user_passwords_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui senhas cadastradas.")
        elif user_passwords_quantity >= 1:
            col1, col2 = st.columns(2)
            user_accounts = self.get_user_accounts_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_option = st.selectbox(
                        label="Selecione a conta",
                        options=user_accounts
                    )
                    safe_password = st.text_input(
                        label="Informe sua senha",
                        type="password",
                        help="Corresponde a senha para acessar a aplicação."
                    )
                    confirm_safe_password = st.text_input(
                        label="Confirme sua senha",
                        type="password",
                        help="Deve ser idêntica a senha informada acima."
                    )
                    confirm_selection = st.checkbox(label="Confirmar seleção")

            account_details_values = (
                selected_option,
                user_id,
                user_document
            )
            result_list = QueryExecutor().complex_consult_query(
                query=account_details_query,
                params=account_details_values
            )
            result_list = QueryExecutor().treat_complex_result(
                values_to_treat=result_list,
                values_to_remove=to_remove_list
            )

            if confirm_selection:
                is_password_valid, hashed_password = Login().check_login(
                    user_id, safe_password
                )
                if (
                    safe_password != ""
                    and confirm_safe_password != ""
                    and safe_password == confirm_safe_password
                    and is_password_valid
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                            body=":white_check_mark: Confirmação de Exclusão"
                        )
                        with st.expander(label="Dados", expanded=True):
                            aux_string = ''
                            for i in range(0, len(result_list)):
                                st.write(field_names[i])
                                aux_string = str(result_list[i])
                                if aux_string.startswith('b'):
                                    aux_string = aux_string[1:]
                                st.code(body="{}".format(aux_string))
                            confirm_delete_selection = st.checkbox(
                                label="Confirmar exclusão"
                            )
                        delete_password_button = st.button(
                            label=":wastebasket: Deletar senha"
                        )

                    if confirm_delete_selection and delete_password_button:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(1.25)

                            delete_password_values = (
                                selected_option,
                                user_id,
                                user_document
                            )
                            QueryExecutor().insert_query(
                                query=delete_password_query,
                                values=delete_password_values,
                                success_message="Senha excluída com sucesso!",
                                error_message="Erro ao excluir senha:"
                            )

                            query_values = (
                                user_id,
                                'Exclusão',
                                'Excluiu a senha do site {}'.format(
                                    selected_option
                                )
                            )
                            QueryExecutor().insert_query(
                                query=log_query,
                                values=query_values,
                                success_message='Log gravado.',
                                error_message='Erro ao gravar log:'
                            )
                    elif (
                            confirm_delete_selection is False
                            and delete_password_button
                    ):
                        with col1:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.warning(body="Confirme a exclusão.")

                elif (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password == confirm_safe_password
                        and is_password_valid is False
                ):
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(body="A senha informada é inválida.")

                elif safe_password != confirm_safe_password:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                                body=":white_check_mark: Validação de Dados"
                            )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(body="As senhas não coincidem.")

    def main_menu(self):
        """
        Menu Principal.
        """
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header(body=":lock: Senhas")

        with col2:
            menu_options = [
                "Cadastrar senha",
                "Consultar senha",
                "Atualizar senha",
                "Deletar senha"
            ]
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

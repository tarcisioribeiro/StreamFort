from dictionary.sql.credit_cards_queries import (
    card_insert_query,
    cards_with_name_query,
    credit_card_data_query,
    delete_card_query,
    search_user_credit_cards_number,
    search_user_credit_cards_names,
    update_card_query
)
from dictionary.sql.other_queries import log_query
from dictionary.vars import to_remove_list, today
from functions.get_actual_time import GetActualTime
from functions.login import Login
from functions.query_executor import QueryExecutor
from functions.validate_document import Documents
from time import sleep
import streamlit as st


class CreditCards:
    """
    Classe que representa os cartões de crédito,
    com as quatro funções básicas de um CRUD.
    """
    def __init__(self):
        self.user_id, self.user_document = Login().get_user_data()

    def check_if_card_name_already_exists(self, credit_card_name: str):
        """
        Verifica se o nome do cartão já foi utilizado anteriormente.

        Returns
        -------
        is_card_name_available : bool
            Se o nome do cartão está disponível ou não.
        """

        is_card_name_available: bool

        query_values = (
            credit_card_name,
            self.user_id,
            self.user_document
        )

        cards_with_name_quantity = QueryExecutor().simple_consult_query(
            query=cards_with_name_query,
            params=query_values
        )
        cards_with_name_quantity = QueryExecutor().treat_simple_result(
            value_to_treat=cards_with_name_quantity,
            values_to_remove=to_remove_list
        )
        cards_with_name_quantity = int(cards_with_name_quantity)

        if cards_with_name_quantity == 0:
            is_card_name_available = True
        else:
            is_card_name_available = False

        return is_card_name_available

    def get_user_credit_cards_number(self):
        """
        Consulta a quantidade de cartões de crédito registrados pelo usuário.

        Returns
        -------
        user_credit_cards_number : int
            Número de cartões registrados pelo cliente.
        """

        user_credit_cards_number = QueryExecutor().simple_consult_query(
            search_user_credit_cards_number,
            params=(
                self.user_id,
                self.user_document
            )
        )
        user_credit_cards_number = QueryExecutor().treat_simple_result(
            user_credit_cards_number,
            to_remove_list
        )
        user_credit_cards_number = int(user_credit_cards_number)

        return user_credit_cards_number

    def get_credit_cards_names(self):
        """
        Consulta o nome dos cartões de crédito do usuário.

        Returns
        -------
        credit_cards_options : list
            Lista com o nome dos cartões.
        """

        credit_cards_options = []

        user_credit_cards_names = QueryExecutor().complex_consult_query(
            search_user_credit_cards_names,
            params=(
                self.user_id,
                self.user_document
            )
        )
        user_credit_cards_names = (
            QueryExecutor().treat_simple_results(
                user_credit_cards_names,
                to_remove_list
            )
        )
        for i in range(0, len(user_credit_cards_names)):
            credit_cards_options.append(user_credit_cards_names[i])

        return credit_cards_options

    def create_new_credit_card(self):
        """
        Função para criação de um novo cartão de cŕedito.
        """

        st.divider()

        def validate_card_values(
                card_name: str,
                card_number: str,
                owner_on_card_name: str,
                expiration_date: str,
                actual_date: str,
                security_code: str
        ):
            if card_name == '':
                st.error("Informe o nome do cartão.")
            if card_number == '':
                st.error("Informe o número do cartão.")
            if " " in card_number:
                st.error(body="Não pode haver espaços vazios no número.")
            if owner_on_card_name == '':
                st.error("Informe o nome do titular no cartão.")
            if expiration_date <= actual_date:
                st.error(body="A data deve ser maior que a data atual.")
            if security_code == '':
                st.error(body="Informe o código de segurança do cartão.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(body=":computer: Entrada de Dados")
            with st.expander(label="Dados do Cartão", expanded=True):
                card_name = st.text_input(
                    label="Nome do cartão",
                    max_chars=100,
                    help="Informe um nome representativo."
                )
                card_number = st.text_input(
                    label="Número do cartão",
                    max_chars=16,
                    help="Informe o número do cartão sem espaços vazios."
                )
                last_card_numbers = card_number[-4:]
                owner_on_card_name = st.text_input(
                    label="Nome do titular",
                    max_chars=100,
                    help="Nome do titular impresso no cartão."
                )
                expiration_date = st.date_input(
                    label="Data de validade",
                    help="Data de validade impressa no cartão."
                )
                str_expiration_date = str(expiration_date)
                security_code = st.text_input(
                    label="Código de segurança",
                    max_chars=3,
                    type="password",
                    key="security_code",
                    help="""
                    Código de segurança do cartão,
                    identificado como CVV ou CCV.
                    """)
                confirm_code = st.text_input(
                    label="Confirmação de código",
                    max_chars=3,
                    type="password",
                    key="confirm_code",
                    help="""Deve corresponder ao código informado acima."""
                )
                confirm_data = st.checkbox(
                    label="Confirmar dados",
                    value=False
                )
                actual_date = GetActualTime().get_actual_data()
            register_button = st.button(label=":floppy_disk: Cadastrar cartão")

            if register_button and confirm_data:
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(1.25)
                if (
                        card_name != ''
                        and card_number != ''
                        and owner_on_card_name != ''
                        and security_code != ''
                        and confirm_code != ''
                        and security_code == confirm_code
                ):
                    with col2:
                        st.subheader(
                            body=":white_check_mark: Validação dos Dados"
                        )
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            valid_card = Documents().validate_credit_card(
                                card_number
                            )
                            if valid_card is False:
                                st.error(body="O número do cartão é inválido.")
                                validate_card_values(
                                    card_name,
                                    card_number,
                                    owner_on_card_name,
                                    str_expiration_date,
                                    actual_date,
                                    security_code
                                )
                            elif valid_card:
                                st.success(body="Número de cartão válido.")
                                if (
                                    owner_on_card_name != ''
                                    and card_name != ''
                                    and security_code != ''
                                    and security_code == confirm_code
                                ):
                                    (
                                        is_card_name_available
                                    ) = self.check_if_card_name_already_exists(
                                        card_name
                                    )
                                    if is_card_name_available:
                                        with col2:
                                            with st.expander(
                                                label="Validação dos dados",
                                                expanded=True
                                            ):
                                                st.success(
                                                    body="Nome válido."
                                                )

                                        card_insert_values = (
                                            card_name,
                                            card_number,
                                            owner_on_card_name,
                                            self.user_id,
                                            self.user_document,
                                            expiration_date,
                                            security_code
                                        )
                                        QueryExecutor().insert_query(
                                            query=card_insert_query,
                                            values=card_insert_values,
                                            success_message="""
                                                Cartão cadastrado.
                                            """,
                                            error_message="""
                                                Erro ao cadastrar cartão:
                                            """
                                        )

                                        log_values = (
                                            self.user_id,
                                            'Cadastro',
                                            '''Cadastrou o cartão {}
                                            com o final {}.'''.format(
                                                card_name,
                                                last_card_numbers
                                            )
                                        )
                                        QueryExecutor().insert_query(
                                            log_query,
                                            log_values,
                                            "Log gravado.",
                                            "Erro ao gravar log:"
                                        )
                                    else:
                                        with col2:
                                            with st.expander(
                                                label="Validação dos dados",
                                                expanded=True
                                            ):
                                                st.error(
                                                    body="""
                                                    O nome já edtá sendo usado.
                                                    """
                                                )

                                elif (
                                        expiration_date <= actual_date
                                        or owner_on_card_name == ''
                                        or card_name == ''
                                        or security_code == ''
                                        or security_code != confirm_code
                                ):
                                    if (
                                        expiration_date <= actual_date
                                        or owner_on_card_name == ''
                                        or card_name == ''
                                        or security_code == ''
                                    ):
                                        validate_card_values(
                                            card_name,
                                            owner_on_card_name,
                                            expiration_date,
                                            actual_date,
                                            security_code
                                        )
                                    if security_code != confirm_code:
                                        with col2:
                                            with st.expander(
                                                label="Validação dos dados",
                                                expanded=True
                                            ):
                                                st.error(
                                                    body='''
                                                    Os códigos não coincidem.
                                                    '''
                                                )

                elif (
                        card_name == ''
                        or card_number == ''
                        or owner_on_card_name == ''
                        or security_code == ''
                        or confirm_code == ''
                ):
                    with col2:
                        st.subheader(
                            body=":white_check_mark: Validação dos Dados"
                        )
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="Há um ou mais campos vazios."
                                )

            elif (
                    register_button
                    and confirm_data is False
            ):
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(0.5)
                    with st.expander(label="Aviso", expanded=True):
                        st.warning(
                            body="Confirme os dados do cartão para prosseguir."
                        )

    def read_credit_cards(self):
        """
        Função para a consulta de um cartão de crédito.
        """

        user_credit_cards_number = self.get_user_credit_cards_number()

        st.divider()

        if user_credit_cards_number > 0:
            col1, col2 = st.columns(2)
            credit_cards_options = self.get_credit_cards_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_user_card = st.selectbox(
                        label="Selecione o cartão",
                        options=credit_cards_options
                    )
                    safe_password = st.text_input(
                        label="Informe sua senha",
                        type="password",
                        help="Corresponde a senha de acesso."
                    )
                    confirm_safe_password = st.text_input(
                        label="Confirme sua senha",
                        type="password",
                        help="Deve ser idêntica a senha informada acima."
                    )
                    confirm_selection = st.checkbox(label="Confirmar seleção")

                consult_button = st.button(
                    label=":file_folder: Consultar cartão")

                if confirm_selection and consult_button:

                    (
                        is_password_valid, hashed_password
                    ) = Login().get_user_password(
                        self.user_id,
                        safe_password
                    )

                    if (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password == confirm_safe_password
                        and is_password_valid
                    ):
                        card_field_names = [
                            "Nome do cartão",
                            "Número do cartão",
                            "Nome do titular no cartão",
                            "Data da validade",
                            "Código de segurança"
                        ]

                        credit_card_data = (
                            QueryExecutor().complex_compund_query(
                                query=credit_card_data_query,
                                list_quantity=4,
                                params=(
                                    self.user_id,
                                    self.user_document,
                                    selected_user_card
                                )
                            )
                        )
                        credit_card_data = (
                            QueryExecutor().treat_simple_results(
                                credit_card_data,
                                to_remove_list
                            )
                        )
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(1.25)
                            st.subheader(
                                body=":white_check_mark: Dados da Consulta"
                            )
                            with st.expander(
                                label="Dados do cartão",
                                expanded=True
                            ):
                                for i in range(0, len(credit_card_data)):
                                    st.write(card_field_names[i])
                                    st.code(credit_card_data[i])

                                last_card_numbers = str(
                                    credit_card_data[1])[-4:]

                                log_values = (
                                    self.user_id,
                                    "Consulta",
                                    """Consultou os dados do
                                    cartão {} com o final {}.
                                    """.format(
                                        credit_card_data[0],
                                        last_card_numbers
                                    )
                                )
                                QueryExecutor().insert_query(
                                    log_query,
                                    log_values,
                                    "Log gravado.",
                                    "Erro ao gravar log:"
                                )

                    elif (
                            safe_password != ""
                            and confirm_safe_password != ""
                            and safe_password == confirm_safe_password
                            and is_password_valid is False
                    ):
                        with col2:
                            st.subheader(
                                body=":white_check_mark: Validação da Consulta"
                            )
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(body="A senha informada é inválida.")

                    elif safe_password != confirm_safe_password:
                        with col2:
                            st.subheader(
                                body=":white_check_mark: Validação da Consulta"
                            )
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="As senhas informadas não coincidem."
                                )

        else:
            col1, col2, col3 = st.columns(3)

            with col2:
                with st.spinner(text="Aguarde..."):
                    sleep(0.5)
                st.warning(body="Você ainda não possui cartões cadastrados.")

    def update_credit_card(self):
        """
        Função para a atualização de um cartão de crédito.
        """

        user_credit_cards_number = self.get_user_credit_cards_number()

        st.divider()

        if user_credit_cards_number > 0:
            col1, col2 = st.columns(2)
            credit_cards_options = self.get_credit_cards_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_user_card = st.selectbox(
                        label="Selecione o cartão",
                        options=credit_cards_options
                    )
                    safe_password = st.text_input(
                        label="Informe sua senha",
                        type="password",
                        help="Corresponde a senha de acesso."
                    )
                    confirm_safe_password = st.text_input(
                        label="Confirme sua senha",
                        type="password",
                        help="Deve ser idêntica a senha informada acima."
                    )
                    confirm_selection = st.checkbox(label="Confirmar seleção")

                if confirm_selection:
                    (
                        is_password_valid,
                        hashed_password
                    ) = Login().get_user_password(
                        self.user_id,
                        safe_password
                    )
                    if (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password == confirm_safe_password
                        and is_password_valid
                    ):

                        credit_card_data = (
                            QueryExecutor().complex_compund_query(
                                query=credit_card_data_query,
                                list_quantity=4,
                                params=(
                                    self.user_id,
                                    self.user_document,
                                    selected_user_card
                                )
                            )
                        )
                        credit_card_data = (
                            QueryExecutor().treat_simple_results(
                                credit_card_data,
                                to_remove_list
                            )
                        )
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.subheader(
                                body="""
                                :white_check_mark: Atualização dos Dados
                                """
                            )
                            with st.expander(
                                label="Novos dados do cartão",
                                expanded=True
                            ):
                                st.info(body="Nome do cartão: {}".format(
                                    selected_user_card))
                                card_number = st.text_input(
                                    label="Número do cartão",
                                    max_chars=16,
                                    help="""
                                    Informe o número do cartão sem espaços.
                                    """
                                )
                                last_card_numbers = card_number[-4:]
                                expiration_date = str(st.date_input(
                                    label="Data de validade",
                                    help="Data de validade impressa no cartão."
                                )
                                )
                                security_code = st.text_input(
                                    label="Código de segurança",
                                    max_chars=3,
                                    type="password",
                                    key="security_code",
                                    help="""
                                    Código de segurança do cartão,
                                    identificado como CVV ou CCV.
                                    """
                                )
                                confirm_code = st.text_input(
                                    label="Confirmação de código",
                                    max_chars=3,
                                    type="password",
                                    key="confirm_code",
                                    help="""
                                    Deve corresponder ao código
                                    informado acima.
                                    """
                                )
                                confirm_data = st.checkbox(
                                    label="Confirmar dados",
                                    value=False
                                )
                            update_card_button = (
                                st.button(label="""{} {}""".format(
                                    ":arrows_counterclockwise:",
                                    "Atualizar cartão"
                                )
                                )
                            )

                            if (
                                confirm_data
                                and update_card_button
                                and security_code == confirm_code
                                and card_number != ""
                                and expiration_date > today
                            ):
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(1.25)
                                    st.subheader(
                                        body="""
                                        :white_check_mark: Validação dos Dados
                                        """
                                    )
                                    with st.expander(
                                        label="Validação dos dados",
                                        expanded=True
                                    ):
                                        is_card_valid = (
                                            Documents().validate_credit_card(
                                                card_number
                                            )
                                        )

                                if is_card_valid:
                                    with col2:
                                        with st.spinner(text="Aguarde..."):
                                            sleep(0.5)
                                        st.subheader(
                                            body="""
                                            :white_check_mark:
                                            Validação dos Dados
                                            """
                                        )
                                        with st.expander(
                                            label="Validação dos dados",
                                            expanded=True
                                        ):
                                            st.success(
                                                body="Número de cartão válido."
                                            )

                                    update_card_values = (
                                        card_number,
                                        expiration_date,
                                        security_code,
                                        selected_user_card
                                    )
                                    QueryExecutor().insert_query(
                                        query=update_card_query,
                                        values=update_card_values,
                                        success_message="Cartão atualizado.",
                                        error_message="""
                                        Erro ao atualizar cartão:
                                        """
                                    )

                                    log_values = (
                                        self.user_id,
                                        "Atualização",
                                        """
                                        Atualizou o cartão {} com o final {}.
                                        """.format(
                                            credit_card_data[0],
                                            last_card_numbers
                                        )
                                    )
                                    QueryExecutor().insert_query(
                                        query=log_query,
                                        values=log_values,
                                        success_message="Log gravado.",
                                        error_message="Erro ao gravar log:"
                                    )
                                elif is_card_valid is False:
                                    with col2:
                                        with st.spinner(text="Aguarde..."):
                                            sleep(0.5)
                                        st.subheader(
                                            body="""
                                            :white_check_mark:
                                            Validação dos Dados
                                            """
                                        )
                                        with st.expander(
                                            label="Validação dos dados",
                                            expanded=True
                                        ):
                                            st.error(
                                                body="""
                                                Número de cartão inválido.
                                                """
                                            )

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
                                body="""
                                :white_check_mark: Validação dos Dados
                                """
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
                                body="""
                                    :white_check_mark: Validação dos Dados
                                    """)
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="As senhas informadas não coincidem."
                                )

        else:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui cartões cadastrados.")

    def delete_credit_card(self):
        """
        Função para a exclusão de um cartão de crédito.
        """

        user_credit_cards_number = self.get_user_credit_cards_number()

        st.divider()

        if user_credit_cards_number > 0:
            col1, col2 = st.columns(2)
            credit_cards_options = self.get_credit_cards_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_user_card = st.selectbox(
                        label="Selecione o cartão",
                        options=credit_cards_options
                    )
                    safe_password = st.text_input(
                        label="Informe sua senha",
                        type="password",
                        help="""
                        Corresponde a senha utilizada para acessar a aplicação.
                        """
                    )
                    confirm_safe_password = st.text_input(
                        label="Confirme sua senha",
                        type="password",
                        help="Deve ser idêntica a senha informada acima."
                    )
                    confirm_selection = st.checkbox(label="Confirmar seleção")
                if confirm_selection:
                    (
                        is_password_valid,
                        hashed_password
                    ) = Login().get_user_password(
                        self.user_id,
                        safe_password
                    )

                    if (
                        confirm_safe_password != ""
                        and safe_password != ""
                        and confirm_safe_password == safe_password
                        and is_password_valid
                    ):
                        card_field_names = [
                            "Cartão",
                            "Nome do titular no cartão",
                            "Data da validade",
                            "Código de segurança"
                        ]

                        credit_card_data = (
                            QueryExecutor().complex_compund_query(
                                query=credit_card_data_query,
                                list_quantity=4,
                                params=(
                                    self.user_id,
                                    self.user_document,
                                    selected_user_card
                                )
                            )
                        )
                        credit_card_data = (
                            QueryExecutor().treat_simple_results(
                                values_to_treat=credit_card_data,
                                values_to_remove=to_remove_list
                            )
                        )
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.subheader(
                                body="""
                                :white_check_mark: Validação da Exclusão
                                """
                            )
                            with st.expander(
                                label="Dados do cartão",
                                expanded=True
                            ):
                                for i in range(0, len(credit_card_data)):
                                    st.write(card_field_names[i])
                                    st.code(credit_card_data[i])
                                confirm_card_exclusion = st.checkbox(
                                    label="Confirmar exclusão")
                            delete_credit_card_button = st.button(
                                label=":wastebasket: Deletar cartão"
                            )
                            if (
                                confirm_card_exclusion
                                and delete_credit_card_button
                            ):
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(1.25)

                                delete_card_values = (
                                    selected_user_card,
                                    self.user_id,
                                    self.user_document
                                )
                                QueryExecutor().insert_query(
                                    query=delete_card_query,
                                    values=delete_card_values,
                                    success_message="Cartão excluído.",
                                    error_message="Erro ao excluir cartão:"
                                )
                                last_card_numbers = str(
                                    credit_card_data[1])[-4:]

                                log_values = (
                                    self.user_id,
                                    "Exclusão",
                                    """
                                    Excluiu o cartão {} com o final {}.
                                    """.format(
                                        credit_card_data[0],
                                        last_card_numbers
                                    )
                                )
                                QueryExecutor().insert_query(
                                    log_query,
                                    log_values,
                                    "Log gravado.",
                                    "Erro ao gravar log:"
                                )

                            elif (
                                    delete_credit_card_button
                                    and confirm_card_exclusion is False
                            ):
                                with col1:
                                    with st.expander(
                                        label="Aviso",
                                        expanded=True
                                    ):
                                        st.warning(
                                            body="""
                                            Confirme a exclusão da senha.
                                            """
                                        )

                    elif (
                            confirm_safe_password != ""
                            and safe_password != ""
                            and confirm_safe_password == safe_password
                            and is_password_valid is False
                    ):
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.subheader(
                                body="""
                                :white_check_mark: Validação da Exclusão
                                """
                            )
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(body="A senha informada é inválida.")
                    if (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password != confirm_safe_password
                    ):
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.subheader(
                                body="""
                                    :white_check_mark: Validação da Exclusão
                                    """
                            )
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="As senhas informadas não coincidem."
                                )

        else:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui cartões cadastrados.")

    def main_menu(self):
        """
        Menu Principal.
        """
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header(body=":credit_card: Cartões")
            menu_options = {
                "Cadastrar cartão": self.create_new_credit_card,
                "Consultar cartão": self.read_credit_cards,
                "Atualizar cartão": self.update_credit_card,
                "Deletar cartão": self.delete_credit_card
            }
        with col2:
            selected_option = st.selectbox(
                label="Menu",
                options=menu_options.keys()
            )
        selected_function = menu_options[selected_option]
        selected_function()

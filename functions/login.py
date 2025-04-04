import streamlit as st
import mysql.connector
import bcrypt
import uuid
from dictionary.vars import absolute_app_path, db_config, to_remove_list
from functions.query_executor import QueryExecutor
from functions.validate_document import Documents
from dictionary.sql import check_user_query
from time import sleep


class CreateUser:
    """
    Classe com métodos para a criação de usuários.
    """

    def hash_password(self, password: str) -> bytes:
        """
        Realiza a encriptação da senha informada pelo usuário.

        Parameters
        ----------
        password : str
            A senha a ser encriptada.

        Returns
        -------
        bytes
            A senha encriptada.
        """

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def is_login_valid(self, login: str):
        """
        Realiza a validação do nome do login escolhido pelo usuário.

        Parameters
        ----------
        login : str
            O nome do login escolhido pelo usuário.

        Returns
        -------
        bool
            Se o nome de login é ou não válido.
        """
        if login != "":
            has_upper = any(c.isupper() for c in login)
            has_digit = any(c.isdigit() for c in login)
            has_special = any(not c.isalnum() for c in login)
            if " " in login or has_upper or has_digit or has_special:
                st.error(body="O login '{}' é inválido.".format(login))
                return False
            else:
                st.success(body="O login '{}' é válido.".format(login))
                return True
        else:
            st.error(body="O login '{}' é inválido.".format(login))
            return False

    def is_password_valid(self, password: str):
        """
        Realiza a validação da senha escolhida pelo usuário.

        Parameters
        ----------
        password : str
            A senha escolhida pelo usuário.

        Returns
        -------
        bool
            Se a senha escolhida é ou não válida.
        """

        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        if (
            " " in password
            or has_upper is False
            or has_digit is False
            or has_special is False
            or len(password) < 8
        ):
            st.error(body="A senha informada é inválida.")
            return False
        else:
            st.success(body="A senha informada é válida.")
            return True

    def main_menu(self):
        """
        Menu principal da criação de usuário.
        """
        logged_user, logged_user_password = Login().get_user_data(
            return_option="user_doc_name"
        )

        query_executor = QueryExecutor()
        document = Documents()

        check_user_quantity = query_executor.simple_consult_brute_query(
            check_user_query
        )
        check_user_quantity = query_executor.treat_simple_result(
            check_user_quantity,
            to_remove_list
        )
        check_user_quantity = int(check_user_quantity)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header(body=":closed_lock_with_key: StreamFort")

        with col2:
            st.header(body=":floppy_disk: Cadastro de usuário")

        st.divider()

        col4, col5, col6 = st.columns(3)

        with col6:
            st.subheader(body=":white_check_mark: Validação de Dados")
            data_validator_expander = st.expander(
                label="Aviso",
                expanded=True
            )

        if check_user_quantity == 0:
            with col6:
                with data_validator_expander:
                    st.warning(body="Cadastre o primeiro usuário.")

        with col4:
            st.subheader(body=":computer: Entrada de Dados")
            with st.expander(label="Dados de login", expanded=True):
                user_login = st.text_input(
                    label="Login de usuário",
                    max_chars=25,
                    help="Deve conter apenas letras minúsculas, sem espaços.",
                )
                user_password = st.text_input(
                    label="Senha de usuário",
                    max_chars=100,
                    help="""A senha deve conter ao mínimo 8 caracteres,
                    1 letra maiúscula, 1 minúscula e 1 caractere especial,
                    sem espaços.""",
                    type="password",
                    key="user_password"
                )
                confirm_user_password = st.text_input(
                    label="Confirmação de senha",
                    max_chars=100,
                    help="Deve ser a mesma informada acima.",
                    type="password",
                    key="confirm_user_password"
                )

            confirm_values = st.checkbox(label="Confirmar dados")

        sex_options = {"Masculino": "M", "Feminino": "F"}

        with col5:
            st.subheader(body=" ")
            with st.expander(label="Dados do usuário", expanded=True):
                user_name = st.text_input(
                    label="Nome de usuário",
                    max_chars=100,
                    help="Informe aqui seu nome completo.",
                )
                user_document = st.text_input(
                    label="Documento do usuário",
                    help="Informe seu CPF neste campo."
                )
                user_sex = st.selectbox(
                    label="Sexo do usuário", options=sex_options.keys())

            insert_new_user_button = st.button(
                label=":floppy_disk: Cadastrar novo usuário"
            )

            if insert_new_user_button:
                user_sex = sex_options[user_sex]
                if confirm_values is True:
                    with st.spinner(text="Aguarde..."):
                        sleep(2.5)
                    with col6:
                        with data_validator_expander:
                            is_document_valid = (
                                document.validate_owner_document(
                                    user_document
                                )
                            )
                            valid_login = self.is_login_valid(user_login)
                            valid_password = self.is_password_valid(
                                user_password)

                    if (
                        user_login != ""
                        and user_password != ""
                        and confirm_user_password != ""
                        and (user_password == confirm_user_password)
                        and user_name != ""
                        and is_document_valid is True
                        and valid_login is True
                        and valid_password is True
                    ):
                        hashed_password = self.hash_password(user_password)
                        if check_user_quantity == 0:
                            insert_new_user_query = """
                            INSERT INTO
                                usuarios (
                                    login,
                                    senha,
                                    nome,
                                    documento_usuario,
                                    sexo
                                )
                            VALUES (%s, %s, %s, %s, %s);"""
                            new_user_values = (
                                user_login,
                                hashed_password,
                                user_name,
                                user_document,
                                user_sex
                            )
                            query_executor.insert_query(
                                insert_new_user_query,
                                new_user_values,
                                "Novo usuário cadastrado com sucesso!",
                                "Erro ao cadastrar novo usuário:"
                            )

                            log_query = '''
                            INSERT INTO
                                seguranca.logs_atividades (
                                    usuario_log,
                                    tipo_log,
                                    conteudo_log
                                )
                            VALUES ( %s, %s, %s);'''
                            log_values = (
                                user_login,
                                "Registro",
                                "O usuário foi cadastrado no sistema."
                            )
                            query_executor.insert_query(
                                log_query,
                                log_values,
                                "Log gravado.",
                                "Erro ao gravar log:"
                            )

                            with st.spinner(text="Recarregando..."):
                                sleep(2.5)
                                st.rerun()

                        elif check_user_quantity >= 1:

                            with col6:
                                check_if_user_document_exists_query = """
                                SELECT
                                    COUNT(id_usuario)
                                FROM
                                    usuarios
                                WHERE
                                    documento_usuario = %s;"""
                                check_if_user_exists = (
                                    query_executor.simple_consult_query(
                                        check_if_user_document_exists_query,
                                        params=(
                                            user_document,
                                        )
                                    )
                                )
                                check_if_user_exists = (
                                    query_executor.treat_simple_result(
                                        check_if_user_exists,
                                        to_remove_list
                                    ))
                                check_if_user_exists = int(
                                    check_if_user_exists
                                )
                                if check_if_user_exists == 0:
                                    insert_new_user_query = """
                                    INSERT INTO
                                        usuarios (
                                            login,
                                            senha,
                                            nome,
                                            documento_usuario,
                                            sexo
                                        )
                                    VALUES (%s, %s, %s, %s, %s);"""
                                    new_user_values = (
                                        user_login,
                                        hashed_password,
                                        user_name,
                                        user_document,
                                        user_sex
                                    )
                                    query_executor.insert_query(
                                        insert_new_user_query,
                                        new_user_values,
                                        "Novo usuário cadastrado com sucesso!",
                                        "Erro ao cadastrar novo usuário:"
                                    )

                                    log_query = '''
                                    INSERT INTO
                                        seguranca.logs_atividades (
                                            usuario_log,
                                            tipo_log,
                                            conteudo_log
                                        )
                                    VALUES ( %s, %s, %s);'''
                                    log_values = (
                                        logged_user,
                                        "Registro",
                                        """
                                            Cadastrou o usuário {} associado
                                            ao documento {} no sistema.
                                        """.format(
                                            user_name,
                                            user_document
                                        )
                                    )
                                    query_executor.insert_query(
                                        log_query,
                                        log_values,
                                        "Log gravado.",
                                        "Erro ao gravar log:"
                                    )

                                    sleep(2)
                                elif check_if_user_exists >= 1:
                                    with data_validator_expander:
                                        st.error("""
                                        Já existe um registro do documento {}.
                                        """.format(
                                            user_document
                                        )
                                        )

                    elif (
                            user_login == ""
                            or user_password == ""
                            or user_name == ""
                            or is_document_valid is False
                            or valid_login is False
                            or valid_password is False
                            or confirm_user_password == ""
                            or (user_password != confirm_user_password)):
                        with col6:
                            if user_login == "":
                                with data_validator_expander:
                                    st.error("O login não foi preenchido.")
                            if user_password == "":
                                with data_validator_expander:
                                    st.error("A senha não foi preenchida.")
                            if user_name == "":
                                with data_validator_expander:
                                    st.error("O nome não foi preenchido.")
                            if confirm_user_password == "":
                                with data_validator_expander:
                                    st.error(
                                        "A confirmação não foi preenchida.")
                            if user_password != confirm_user_password and (
                                user_password != ""
                                and confirm_user_password != ""
                            ):
                                with data_validator_expander:
                                    st.error(
                                        "As senhas informadas não coincidem.")

                elif confirm_values is False:
                    with col6:
                        with data_validator_expander:
                            st.warning(
                                body="Revise os dados antes de prosseguir."
                            )


class Login:
    """
    Classe com métodos para a validação de login e usuário.
    """

    def get_user_data(self, return_option: str):
        """
        Faz a consulta dos dados do usuário,
        de acordo com a opção de dados retornados selecionada.

        Parameters
        ----------
        return_option : str
            Define os dados que serão retornados pela função.

        Returns
        -------
        user_name : str
            Nome completo do usuário logado.
        user_document : str
            Documento do usuário logado.
        """
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        user_login_query = ""
        user_data_query = ""

        if return_option == "user_doc_name":
            user_data_query = """
            SELECT usuarios.nome, usuarios.documento_usuario
            FROM usuarios
            INNER JOIN usuarios_logados
            ON usuarios.id_usuario = usuarios_logados.usuario_id
            WHERE usuarios_logados.sessao_id = %s;
            """

            user_data = QueryExecutor().complex_compund_query(
                query=user_data_query,
                list_quantity=2,
                params=(
                    st.session_state.session_id,
                )
            )
            user_data = QueryExecutor().treat_complex_result(
                values_to_treat=user_data, values_to_remove=to_remove_list)

            user_name = user_data[0]
            user_document = user_data[1]

            return user_name, user_document

        elif return_option == "user_login_password":

            user_login_query = """
            SELECT usuarios.login, usuarios.senha
            FROM usuarios
            INNER JOIN usuarios_logados
            ON usuarios.id_usuario = usuarios_logados.usuario_id
            WHERE usuarios_logados.sessao_id = %s
            """

            user_login_data = QueryExecutor().complex_compund_query(
                query=user_login_query,
                list_quantity=2,
                params=(
                    st.session_state.session_id,
                )
            )
            user_login_data = QueryExecutor().treat_complex_result(
                values_to_treat=user_login_data,
                values_to_remove=to_remove_list
            )

            user_login = user_login_data[0]
            user_password = str(user_login_data[1])

            if user_password.startswith('b'):
                user_password = user_password[1:]

            return user_login, user_password

        else:
            st.error(body="Parâmetro não reconhecido.")

    def check_login(self, user, password):
        """
        Valida o login do usuário.

        Parameters
        ----------
        user
            Nome do usuário que está realizando o login.
        password
            Senha do usuário que está realizando o login.

        Returns
        -------
        bool
            A validade do login.
        hashed_password : str
            A senha do usuário encriptada.
        """
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT senha FROM usuarios WHERE login = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]
            return (
                bcrypt.checkpw(
                    password.encode('utf-8'),
                    hashed_password
                ),
                hashed_password)
        return False, '0'

    def register_login(
            self,
            logged_user_id: int,
            logged_user_name: str,
            logged_user_document: str
    ):
        """
        Registra a sessão do usuário no banco de dados.

        Paramaters
        ----------
        logged_user_id : int
            ID do usuário que está presente na tabela 'usuarios'.
        logged_user_name : str
            Nome completo do usuário, presente na tabela 'usuarios'.
        logged_user_document : str
            Documento do usuário, presente na tabela 'usuarios'.
        """
        session_id = str(uuid.uuid4())

        register_session_query = """
        INSERT INTO
            usuarios_logados (
                usuario_id,
                nome_completo,
                documento,
                sessao_id
            )
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY
        UPDATE
            data_login = CURRENT_TIMESTAMP,
            sessao_id = VALUES(sessao_id);
        """
        session_values = (
            logged_user_id,
            logged_user_name,
            logged_user_document,
            session_id
        )

        QueryExecutor.insert_query(
            self,
            query=register_session_query,
            values=session_values,
            success_message="Sessão registrada.",
            error_message="Erro ao registrar sessão:"
        )

        sleep(1.25)

        st.session_state.usuario_id = logged_user_id
        st.session_state.session_id = session_id

    def check_user(self, logged_user: str, logged_user_password: str):
        """
        Realiza a busca dos dados pessoais do usuário logado.

        Returns
        -------
        name : str
            O nome do usuário.
        sex : str
            O sexo do usuário.
        """

        logged_user, logged_user_password = Login().get_user_data(
            return_option="user_login_password")

        name_query: str = """
        SELECT
            nome
        FROM
            usuarios
        WHERE
            login = %s
        AND senha = %s;"""
        sex_query: str = """
        SELECT
            sexo
        FROM
            usuarios
        WHERE
            login = %s
        AND senha = %s;"""

        query_executor = QueryExecutor()

        name = query_executor.simple_consult_query(
            query=name_query, params=(logged_user, logged_user_password))
        name = query_executor.treat_simple_result(name, to_remove_list)

        sex = query_executor.simple_consult_query(
            query=sex_query, params=(logged_user, logged_user_password))
        sex = query_executor.treat_simple_result(sex, to_remove_list)

        return name, sex

    def show_user(self, name: str, sex: str):
        """
        Exibe o avatar e nome do usuário.

        Parameters
        ----------
        name: str
            O nome do usuário.
        sex: str
            O sexo do usuário.
        """
        if sex == "M":
            st.image(image="{}/library/images/man.png".format(
                absolute_app_path
            )
            )
        elif sex == "F":
            st.image(image="{}/library/images/woman.png".format(
                absolute_app_path
            )
            )
        st.text(body="{}".format(name))
        st.divider()

    def main_menu(self):
        """
        Realiza a coleta dos dados de login do usuário.
        """
        query_executor = QueryExecutor()
        col1, col2, col3 = st.columns(3)

        with col2:

            st.header(body=":key: StreamFort")

            with st.container():
                with st.expander(label=":computer: Login", expanded=True):

                    user = st.text_input(":closed_lock_with_key: Usuário")
                    password = st.text_input(":key: Senha", type="password")
                    login_button = st.button(label=":unlock: Entrar")

                    is_login_valid, hashed_password = self.check_login(
                        user, password)

                    if login_button:
                        if is_login_valid:
                            with st.spinner("Aguarde..."):
                                sleep(1)
                                st.toast("Login bem-sucedido!")

                                log_query = '''
                                INSERT INTO
                                    logs_atividades (
                                    usuario_log,
                                    tipo_log,
                                    conteudo_log
                                )
                                VALUES (%s, %s, %s);'''
                                log_values = (user, 'Acesso',
                                              'O usuário acessou o sistema.')
                                query_executor.insert_query(
                                    log_query,
                                    log_values,
                                    "Log gravado.",
                                    "Erro ao gravar log:"
                                )

                                name_doc_query = """
                                SELECT
                                    id_usuario, nome, documento_usuario
                                FROM
                                    usuarios
                                WHERE
                                    login = %s AND senha = %s;
                                """

                                user_name_doc = (
                                    QueryExecutor().complex_compund_query(
                                        query=name_doc_query,
                                        list_quantity=3,
                                        params=(
                                            user,
                                            hashed_password
                                        )
                                    )
                                )
                                user_name_doc = (
                                    QueryExecutor().treat_numerous_simple_result(
                                        user_name_doc,
                                        to_remove_list
                                    )
                                )

                                user_id = int(user_name_doc[0])
                                user_name = str(user_name_doc[1])
                                user_document = str(user_name_doc[2])

                                self.register_login(
                                    logged_user_id=user_id,
                                    logged_user_name=user_name,
                                    logged_user_document=user_document
                                )

                            st.session_state.is_logged_in = True
                            st.rerun()

                        else:
                            st.error(
                                "Login falhou. Verifique suas credenciais.")


class Menu():
    def main_menu(self):
        sidebar = st.sidebar

        with sidebar:
            sidebar_options = {
                "Login": Login,
                "Cadastro de usuário": CreateUser,
            }
            st.image("{}/library/images/key.png".format(absolute_app_path))

            st.divider()

            selected_class = sidebar_options[st.selectbox(
                label="Menu", options=sidebar_options.keys())]

        selected_class().main_menu()

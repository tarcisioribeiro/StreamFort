from dictionary.sql.archive_queries import (
    archive_content_query,
    archives_with_name_query,
    delete_archive_query,
    insert_archive_query,
    search_user_archives_quantity,
    search_user_archives_name
)
from dictionary.sql.other_queries import log_query
from dictionary.user_data import user_id, user_document
from dictionary.vars import to_remove_list, to_remove_archive_list
from functions.login import Login
from functions.query_executor import QueryExecutor
from time import sleep
import streamlit as st


class Archives:
    """
    Classe que representa os arquivos,
    com as quatro funções básicas de um CRUD.
    """

    def check_if_archive_already_exists(self, archive_name: str):
        """
        Verifica se o nome do arquivo já foi utilizado anteriormente.

        Returns
        -------
        is_archive_name_available (bool): Se o nome do arquivo está disponível.
        """
        is_archive_name_available: bool

        query_values = (archive_name, user_id, user_document)

        archives_with_name_quantity = QueryExecutor().simple_consult_query(
            query=archives_with_name_query,
            params=query_values
        )
        archives_with_name_quantity = QueryExecutor().treat_simple_result(
            value_to_treat=archives_with_name_quantity,
            values_to_remove=to_remove_list
        )
        archives_with_parameter_name_quantity = int(
            archives_with_name_quantity
        )

        if archives_with_parameter_name_quantity == 0:
            is_archive_name_available = True
        else:
            is_archive_name_available = False

        return is_archive_name_available

    def get_user_archives_quantity(self):
        """
        Consulta a quantidade de arquivos registrados pelo usuário.

        Returns
        -------
        user_archives_quantity (int): A quantidade de arquivos registrados.
        """

        user_archives_quantity = QueryExecutor().simple_consult_query(
            search_user_archives_quantity,
            params=(user_id, user_document)
        )
        user_archives_quantity = QueryExecutor().treat_simple_result(
            user_archives_quantity, to_remove_list)
        user_archives_quantity = int(user_archives_quantity)

        return user_archives_quantity

    def get_archives_names(self):
        """
        Consulta o nome dos arquivos.

        Returns
        -------
        archives_names (list): A lista com o nome dos arquivos.
        """

        archives_names = []
        user_archives_name = QueryExecutor().complex_consult_query(
            search_user_archives_name,
            params=(user_id, user_document)
        )
        user_archives_name = QueryExecutor().treat_simple_results(
            user_archives_name,
            to_remove_list
        )

        for i in range(0, len(user_archives_name)):
            archives_names.append(user_archives_name[i])

        return archives_names

    def create_new_archive(self):
        """
        Função para criação de um novo arquivo.
        """

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(body=":computer: Entrada de Dados")
            with st.expander(label="Entrada de Dados", expanded=True):
                archive_name = st.text_input(
                    label="Nome do arquivo",
                    max_chars=100,
                    help="Necessário definir um nome para consulta."
                )
                uploaded_file = st.file_uploader(
                    label="Escolha um arquivo de texto",
                    type=["txt"],
                    help="São permitidos arquivos de texto."
                )

                content = None

                if uploaded_file:
                    content = uploaded_file.read().decode("utf-8")
                    with col2:
                        with st.spinner(text="Carregando arquivo..."):
                            sleep(1.25)
                        st.subheader(
                            body=":white_check_mark: Validação do Arquivo")
                        if content != "":
                            with st.expander(
                                label="Conteudo do arquivo carregado",
                                expanded=True
                            ):
                                st.info(content)
                        elif content == "":
                            with col2:
                                st.error(
                                    body="O Conteudo do arquivo está vazio.")

            register_archive_button = st.button(
                ":floppy_disk: Fazer upload do arquivo"
            )
            if register_archive_button:
                if (
                    uploaded_file is not None
                    and content != ""
                    and archive_name != ""
                ):
                    (
                        is_name_available
                    ) = self.check_if_archive_already_exists(
                        archive_name=archive_name
                    )

                    if is_name_available:
                        with col2:
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.success(body="Nome de arquivo disponível.")

                        archive_values = (
                            archive_name,
                            content,
                            user_id,
                            user_document
                        )

                    if content is not None:
                        QueryExecutor().insert_query(
                            insert_archive_query,
                            archive_values,
                            "Upload do arquivo realizado com sucesso!",
                            "Erro ao fazer upload do arquivo:"
                        )

                        log_query_values = (
                            user_id,
                            "Cadastro",
                            "Fez o upload do arquivo {}.".format(
                                archive_name
                            )
                        )
                        QueryExecutor().insert_query(
                            log_query,
                            log_query_values,
                            "Log gravado.",
                            "Erro ao gravar log:"
                        )
                elif (
                    uploaded_file is None
                    or content == ""
                    or archive_name == ""
                ):
                    with col2:
                        with st.spinner(text=""):
                            sleep(1.25)
                        st.subheader(
                            body=":white_check_mark: Validação do Arquivo")
                        if uploaded_file is None:
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="Não foi feito o upload."
                                )
                        if archive_name == "":
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="Não foi informado um nome."
                                )
                else:
                    with col2:
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.error(
                                body="O nome do arquivo já está sendo usado."
                            )

            elif register_archive_button is False:
                pass

    def read_archive(self):
        """
        Função para a consulta de um arquivo.
        """

        user_archives_quantity = self.get_user_archives_quantity()

        if user_archives_quantity >= 1:
            col1, col2 = st.columns(2)

            archives_names = self.get_archives_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_archive = st.selectbox(
                        label="Selecione o arquivo", options=archives_names)
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
                    confirm_selection = st.checkbox(
                        label="Confirmar dados", value=False)

                consult_button = st.button(
                    label=":file_folder: Consultar arquivo")

                if consult_button and confirm_selection:
                    is_password_valid, hashed_password = (
                        Login().get_user_password(
                            user_id,
                            safe_password
                        )
                    )

                    if (
                        safe_password != ""
                        and confirm_safe_password != ""
                        and safe_password == confirm_safe_password
                        and is_password_valid is True
                    ):
                        with st.spinner(text="Aguarde..."):
                            sleep(1.25)

                            archive_content = (
                                QueryExecutor().simple_consult_query(
                                    archive_content_query,
                                    params=(
                                        selected_archive,
                                        user_id,
                                        user_document
                                    )
                                )
                            )
                            archive_content = (
                                QueryExecutor().treat_simple_result(
                                    archive_content,
                                    to_remove_archive_list
                                )
                            )
                            archive_content = archive_content.replace(
                                "\\n", " ")
                            archive_content = archive_content.replace(
                                "  ", " ")
                            archive_content = archive_content.split(" ")

                            for i in range(0, len(archive_content)):
                                if archive_content[i] == "":
                                    del archive_content[i]

                            with col2:
                                st.subheader(
                                    body=":white_check_mark: Dados do Arquivo"
                                )
                                with st.expander(
                                    label="Conteudo",
                                    expanded=True
                                ):
                                    display_content = ""
                                    for i in range(0, len(archive_content)):
                                        display_content += str(
                                            archive_content[i]) + "\n\n"
                                    st.code(display_content)

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
                                body=":white_check_mark: Dados do Arquivo"
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
                                body=":white_check_mark: Dados do Arquivo")
                            with st.expander(
                                label="Validação dos dados",
                                expanded=True
                            ):
                                st.error(
                                    body="As senhas informadas não coincidem.")

                elif consult_button and confirm_selection is False:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.subheader(
                            body=":white_check_mark: Dados do Arquivo")
                        with st.expander(
                            label="Validação dos dados",
                            expanded=True
                        ):
                            st.warning(body="Confirme a seleção dos dados.")

        elif user_archives_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui arquivos registrados.")

    def update_archive(self):
        """
        Função para a atualização de um arquivo.
        """

        user_archives_quantity = self.get_user_archives_quantity()

        if user_archives_quantity >= 1:
            col1, col2 = st.columns(2)

            archives_names = self.get_archives_names()

            with col1:
                st.subheader(body=":computer: Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_archive = st.selectbox(
                        label="Selecione o arquivo", options=archives_names)
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
                    confirm_selection = st.checkbox(
                        label="Confirmar dados", value=False)

                    if confirm_selection:
                        (
                            is_password_valid,
                            hashed_password
                        ) = Login().get_user_password(user_id, safe_password)

                        if (
                            safe_password != ""
                            and confirm_safe_password != ""
                            and safe_password == confirm_safe_password
                            and is_password_valid is True
                        ):
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)

                            archive_content = (
                                QueryExecutor().complex_compund_query(
                                    query=archive_content_query,
                                    list_quantity=2,
                                    params=(
                                        selected_archive,
                                        user_id,
                                        user_document
                                    )
                                )
                            )
                            archive_content = (
                                QueryExecutor().treat_complex_result(
                                    archive_content,
                                    to_remove_archive_list
                                )
                            )

                            for i in range(0, len(archive_content)):
                                if archive_content[i] == "":
                                    del archive_content[i]

                            with col1:
                                with st.expander(
                                    label="Conteudo",
                                    expanded=True
                                ):

                                    display_content = ""
                                    for i in range(0, len(archive_content)):
                                        display_content += str(
                                            archive_content[i]) + "\n\n"

                                    st.code(display_content)

                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                st.subheader(
                                    body=":white_check_mark: Novos Dados"
                                )
                                with st.expander(
                                    label="Novos dados",
                                    expanded=True
                                ):
                                    new_archive_name = st.text_input(
                                        label="Novo nome do arquivo",
                                        max_chars=100,
                                        help="É necessário definir um nome."
                                    )
                                    new_uploaded_file = st.file_uploader(
                                        label="Escolha um arquivo de texto",
                                        type=["txt"],
                                        help="Carregue um arquivo de texto."
                                    )
                                    confirm_new_data = st.checkbox(
                                        label="Confirmar novos dados"
                                    )

                                    content = None

                                    if new_uploaded_file:
                                        (
                                            content
                                        ) = new_uploaded_file.read().decode(
                                            "utf-8"
                                        )
                                        with col2:
                                            with st.spinner(
                                                text="Carregando arquivo..."
                                            ):
                                                sleep(0.5)
                                            if content != "":
                                                with st.expander(
                                                    label="Conteúdo",
                                                    expanded=True
                                                ):
                                                    st.info(content)
                                            elif content == "":
                                                with col2:
                                                    st.error(
                                                        body="Arquivo vazio."
                                                    )

                                update_archive_button = st.button(
                                    label="{} Atualizar arquivo".format(
                                        ":arrows_counterclockwise:"
                                    )
                                )

                            if confirm_new_data and update_archive_button:

                                with st.spinner(text="Aguarde..."):
                                    sleep(1.25)

                                if (
                                    new_archive_name != ""
                                    and content is not None
                                ):
                                    (
                                        is_name_available
                                    ) = self.check_if_archive_name_exists(
                                        archive_name=new_archive_name
                                    )

                                    if is_name_available:
                                        with col1:
                                            with st.expander(
                                                label="Validação dos dados",
                                                expanded=True
                                            ):
                                                st.success(
                                                    body="Nome disponível."
                                                )

                                        archive_values = (
                                            new_archive_name,
                                            content,
                                            user_id,
                                            user_document
                                        )

                                        if content is not None:
                                            QueryExecutor().insert_query(
                                                insert_archive_query,
                                                archive_values,
                                                "Upload realizado.",
                                                "Erro ao fazer upload:"
                                            )

                                            log_query_values = (
                                                user_id,
                                                "Atualização",
                                                "Arquivo {} alterado.".format(
                                                    new_archive_name
                                                )
                                            )
                                            QueryExecutor().insert_query(
                                                log_query,
                                                log_query_values,
                                                "Log gravado.",
                                                "Erro ao gravar log:"
                                            )

                                    else:
                                        with col1:
                                            with st.expander(
                                                label="Validação dos dados",
                                                expanded=True
                                            ):
                                                st.error(
                                                    body="Nome já em uso."
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
                                with st.expander(
                                    label="Validação dos dados",
                                    expanded=True
                                ):
                                    st.error(
                                        body="A senha informada é ínválida.")

                        if safe_password != confirm_safe_password:
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                with st.expander(
                                    label="Validação dos dados",
                                    expanded=True
                                ):
                                    st.error(
                                        body="As senhas não coincidem."
                                    )

        elif user_archives_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.warning(body="Você ainda não possui arquivos registrados.")

    def delete_archive(self):
        """
        Função para a exclusão de um arquivo.
        """

        user_archives_quantity = self.get_user_archives_quantity()

        if user_archives_quantity >= 1:
            col1, col2 = st.columns(2)

            archives_names = self.get_archives_names()

            with col1:
                st.subheader(body="Entrada de Dados")
                with st.expander(label="Consulta", expanded=True):
                    selected_archive = st.selectbox(
                        label="Selecione o arquivo", options=archives_names)
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
                    confirm_selection = st.checkbox(
                        label="Confirmar dados", value=False)

                    if confirm_selection:
                        (
                            is_password_valid, hashed_password
                        ) = Login().get_user_password(user_id, safe_password)
                        if (
                            safe_password != ""
                            and confirm_safe_password != ""
                            and confirm_safe_password == safe_password
                            and is_password_valid
                        ):
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)

                            archive_content = (
                                QueryExecutor().complex_compund_query(
                                    query=archive_content_query,
                                    list_quantity=2,
                                    params=(
                                        selected_archive,
                                        user_id,
                                        user_document
                                    )
                                )
                            )
                            archive_content = (
                                QueryExecutor().treat_complex_result(
                                    archive_content,
                                    to_remove_archive_list
                                )
                            )

                            for i in range(0, len(archive_content)):
                                if archive_content[i] == "":
                                    del archive_content[i]

                            with col2:
                                st.subheader(
                                    body="""
                                    :white_check_mark: Validação de Exclusão
                                    """
                                )
                                with st.expander(
                                    label="Conteudo",
                                    expanded=True
                                ):
                                    display_content = ""
                                    for i in range(0, len(archive_content)):
                                        if "\\n" in archive_content[i]:
                                            display_content = str(
                                                archive_content[i])
                                            (
                                                display_content
                                            ) = display_content.replace(
                                                "\\n", " ")
                                        else:
                                            display_content += str(
                                                archive_content[i]) + "\n\n"

                                    st.code(display_content)
                                    confirm_data_deletion = st.checkbox(
                                        label="Confirmar exclusão dos dados")
                                delete_archive_button = st.button(
                                    label=":wastebasket: Deletar arquivo")

                            if confirm_data_deletion and delete_archive_button:
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(1.25)

                                    archive_values = (
                                        selected_archive,
                                        user_id,
                                        user_document
                                    )

                                    QueryExecutor().insert_query(
                                        delete_archive_query,
                                        archive_values,
                                        "Arquivo deletado com sucesso!",
                                        "Erro ao deletar arquivo:"
                                    )

                                    log_query_values = (
                                        user_id,
                                        "Exclusão",
                                        "Arquivo {} excluído.".format(
                                            selected_archive
                                        )
                                    )
                                    QueryExecutor().insert_query(
                                        log_query,
                                        log_query_values,
                                        "Log gravado.",
                                        "Erro ao gravar log:"
                                    )

                        elif (
                                safe_password != ""
                                and confirm_safe_password != ""
                                and confirm_safe_password == safe_password
                                and is_password_valid is False
                        ):
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                st.subheader(
                                    body="""
                                    :white_check_mark: Validação de Exclusão
                                    """
                                )
                                with st.expander(
                                    label="Validação dos dados",
                                    expanded=True
                                ):
                                    st.error(
                                        body="A senha informada é inválida.")
                        elif safe_password != confirm_safe_password:
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                st.subheader(
                                    body="""
                                    :white_check_mark: Validação de Exclusão
                                    """
                                )
                                with st.expander(
                                    label="Validação dos dados",
                                    expanded=True
                                ):
                                    st.error(
                                        body="As senhas não coincidem."
                                    )

        elif user_archives_quantity == 0:
            col1, col2, col3 = st.columns(3)
            with col2:
                with st.spinner(text="Aguarde..."):
                    sleep(0.5)
                st.warning(body="Você ainda não possui arquivos registrados.")

    def main_menu(self):
        """
        Menu principal.
        """

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header(body=":spiral_note_pad: Arquivos")

        with col2:
            menu_options = {
                "Registrar arquivo": self.create_new_archive,
                "Consultar arquivo": self.read_archive,
                "Atualizar arquivo": self.update_archive,
                "Deletar arquivo": self.delete_archive
            }

            selected_option = st.selectbox(
                label="Menu",
                options=menu_options.keys()
            )

        called_function = menu_options[selected_option]

        st.divider()

        called_function()

from data.session_state import logged_user, logged_user_password
from data.user_data import logged_user_name, logged_user_document
from dictionary.sql import search_user_archives_quantity, search_user_archives_name
from dictionary.vars import to_remove_list, to_remove_archive_list
from functions.query_executor import QueryExecutor
from functions.variables import Variables
from time import sleep
import streamlit as st


class Archives:

    def __init__(self):

        query_executor = QueryExecutor()
        variable = Variables()

        def show_archive():

            user_archives_quantity = query_executor.simple_consult_query(search_user_archives_quantity)
            user_archives_quantity = query_executor.treat_simple_result(user_archives_quantity, to_remove_list)
            user_archives_quantity = int(user_archives_quantity)

            if user_archives_quantity >= 1:

                col1, col2, col3 = st.columns(3)

                archives_names = ["Selecione uma opção"]
                user_archives_name = query_executor.complex_consult_query(search_user_archives_name)
                user_archives_name = query_executor.treat_numerous_simple_result(user_archives_name, to_remove_list)

                for i in range(0, len(user_archives_name)):
                    archives_names.append(user_archives_name[i])

                with col2:

                    with st.expander(label="Consulta", expanded=True):
                        selected_archive = st.selectbox(label="Selecione o arquivo", options=archives_names)
                        safe_password = st.text_input(label="Senha do cofre", type="password")
                        confirm_selection = st.checkbox(label="Confirmar dados", value=False)

                    consult_button = st.button(label=":file_folder: Consultar arquivo")

                    if consult_button:

                        with st.spinner(text="Aguarde..."):
                            sleep(2.5)

                        if confirm_selection == True:
                            if selected_archive == "Selecione uma opção":
                                st.error(body="Selecione uma opção válida.")
                            elif selected_archive != "Selecione uma opção":
                                if safe_password == logged_user_password:
                                    archive_content_query = """SELECT 
                                                                    arquivo_texto.conteudo
                                                                FROM
                                                                    arquivo_texto
                                                                        INNER JOIN
                                                                    usuarios ON arquivo_texto.usuario_associado = usuarios.nome
                                                                        AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
                                                                WHERE
                                                                    arquivo_texto.nome_arquivo = '{}'
                                                                    AND
                                                                    usuarios.login = '{}'
                                                                        AND usuarios.senha = '{}';
                                                                """.format(selected_archive,logged_user,logged_user_password)

                                    archive_content = (query_executor.simple_consult_query(archive_content_query))
                                    archive_content = (query_executor.treat_simple_result(archive_content, to_remove_archive_list))
                                    archive_content = archive_content.replace("\\n", " ")
                                    archive_content = archive_content.replace("  ", " ")
                                    archive_content = archive_content.split(" ")

                                    for i in range(0, len(archive_content)):
                                        if archive_content[i] == "":
                                            del archive_content[i]

                                    with col2:
                                        with st.expander(label="Conteúdo", expanded=True):

                                            display_content = ""
                                            for i in range(0, len(archive_content)):
                                                display_content += str(archive_content[i]) + "\n\n"
                                            
                                            st.write(display_content)

                                        log_query = """INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)"""
                                        log_values = (logged_user, 'Consulta', "Consultou o arquivo {}.".format(selected_archive))
                                        query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

                                elif safe_password != logged_user_password:
                                    st.error(body="A senha do cofre está incorreta.")

                        elif confirm_selection == False:
                            st.error(body="Confirme a seleção dos dados.")

            elif user_archives_quantity == 0:
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.warning(body="Você ainda não possui arquivos registrados.")

        def get_new_archive():

            col1, col2, col3 = st.columns(3)

            with col2:

                with st.expander(label="Entrada de Dados", expanded=True):
                    archive_name = st.text_input(label="Nome do arquivo", max_chars=100)
                    archive_comentary = st.text_input(label="Comentário", max_chars=255)
                    uploaded_file = st.file_uploader(label="Escolha um arquivo de texto", type=["txt"])

                    content = None

                    if uploaded_file:
                        content = uploaded_file.read().decode("utf-8")
                        with col2:
                            with st.expander(label="Arquivo carregado", expanded=True):
                                st.info(content)

                if st.button(":floppy_disk: Fazer upload do arquivo") and uploaded_file is not None:

                    archive_query = "INSERT INTO arquivo_texto (nome_arquivo, conteudo, usuario_associado, documento_usuario_associado) VALUES (%s, %s, %s, %s)"
                    archive_values = (archive_name,content,logged_user_name,logged_user_document)

                    if content is not None:

                        query_executor.insert_query(archive_query, archive_values, "Upload do arquivo realizado com sucesso!", "Erro ao fazer upload do arquivo:")

                        log_query = """INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)"""
                        log_query_values = (logged_user, "Cadastro", "Fez o upload do arquivo {}.".format(archive_name))
                        query_executor.insert_query(log_query, log_query_values, "Log gravado.", "Erro ao gravar log:")

        def archives_main_menu():

            col1, col2, col3 = st.columns(3)

            with col2:
                menu_options = ["Registrar arquivo", "Consultar arquivo"]

                selected_option = st.selectbox(label="Menu", options=menu_options)

            st.divider()
            if selected_option == menu_options[0]:
                get_new_archive()
            elif selected_option == menu_options[1]:
                show_archive()

        self.main_menu = archives_main_menu

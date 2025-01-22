from data.session_state import logged_user
from data.user_data import logged_user_name, logged_user_document
from dictionary.sql import search_user_archives_quantity, search_user_archives_name
from dictionary.vars import to_remove_list, to_remove_archive_list
from functions.query_executor import QueryExecutor
from functions.login import User
from functions.variables import Variables
from time import sleep
import streamlit as st


class Archives:

    def __init__(self):

        query_executor = QueryExecutor()
        variable = Variables()
        user = User()
        
        def create_new_archive():

            col1, col2, col3 = st.columns(3)

            with col1:

                with st.expander(label="Entrada de Dados", expanded=True):
                    archive_name = st.text_input(label="Nome do arquivo", max_chars=100, help="É necessário definir um nome para identificação e consulta posterior.")
                    uploaded_file = st.file_uploader(label="Escolha um arquivo de texto", type=["txt"], help="São permitidos arquivos de texto, na extensão '.txt'. O tamanho do arquivo não pode exceder 200 MB.")

                    content = None

                    if uploaded_file:
                        content = uploaded_file.read().decode("utf-8")
                        with col2:
                            with st.spinner(text="Carregando arquivo..."):
                                sleep(2.5)
                            if content != "":
                                with st.expander(label="Conteudo do arquivo carregado", expanded=True):
                                    st.info(content)
                            elif content == "":
                                with col2:
                                    st.error(body="O Conteudo do arquivo está vazio.")

                register_archive_button = st.button(":floppy_disk: Fazer upload do arquivo")

                if register_archive_button and uploaded_file is not None and content != "" and archive_name != "":

                    archive_query = "INSERT INTO arquivo_texto (nome_arquivo, conteudo, usuario_associado, documento_usuario_associado) VALUES (%s, %s, %s, %s)"
                    archive_values = (archive_name,content,logged_user_name,logged_user_document)

                    if content is not None:

                        query_executor.insert_query(archive_query, archive_values, "Upload do arquivo realizado com sucesso!", "Erro ao fazer upload do arquivo:")

                        log_query = """INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)"""
                        log_query_values = (logged_user, "Cadastro", "Fez o upload do arquivo {}.".format(archive_name))
                        query_executor.insert_query(log_query, log_query_values, "Log gravado.", "Erro ao gravar log:")
                
                elif register_archive_button and (uploaded_file is None or content == "" or archive_name == ""):

                        with col2:
                            with st.spinner(text=""):
                                sleep(2.5)

                            if uploaded_file is None:
                                st.error(body="Não foi feito o upload de um arquivo.")
                            if archive_name == "":
                                st.error(body="Não foi informado um nome para o arquivo.")

        def read_archive():

            user_archives_quantity = query_executor.simple_consult_query(search_user_archives_quantity, params=(logged_user_name, logged_user_document))
            user_archives_quantity = query_executor.treat_simple_result(user_archives_quantity, to_remove_list)
            user_archives_quantity = int(user_archives_quantity)

            if user_archives_quantity >= 1:

                col1, col2 = st.columns(2)

                archives_names = []
                user_archives_name = query_executor.complex_consult_query(search_user_archives_name, params=(logged_user_name, logged_user_document))
                user_archives_name = query_executor.treat_numerous_simple_result(user_archives_name, to_remove_list)

                for i in range(0, len(user_archives_name)):
                    archives_names.append(user_archives_name[i])

                with col1:

                    with st.expander(label="Consulta", expanded=True):
                        selected_archive = st.selectbox(label="Selecione o arquivo", options=archives_names)
                        safe_password = st.text_input(label="Informe sua senha", type="password")
                        confirm_safe_password = st.text_input(label="Confirme sua senha", type="password")
                        confirm_selection = st.checkbox(label="Confirmar dados", value=False)

                    consult_button = st.button(label=":file_folder: Consultar arquivo")

                    if consult_button and confirm_selection:

                        is_password_valid, hashed_password = user.check_login(logged_user, safe_password)

                        if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:

                            with st.spinner(text="Aguarde..."):
                                sleep(2.5)

                                archive_content_query = """
                                SELECT 
                                    arquivo_texto.conteudo
                                FROM
                                    arquivo_texto
                                INNER JOIN
                                    usuarios ON arquivo_texto.usuario_associado = usuarios.nome
                                AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
                                WHERE
                                    arquivo_texto.nome_arquivo = %s
                                AND
                                    arquivo_texto.usuario_associado = %s
                                AND
                                    arquivo_texto.documento_usuario_associado = %s;"""

                                archive_content = (query_executor.simple_consult_query(archive_content_query, params=(selected_archive, logged_user_name, logged_user_document)))
                                archive_content = (query_executor.treat_simple_result(archive_content, to_remove_archive_list))
                                archive_content = archive_content.replace("\\n", " ")
                                archive_content = archive_content.replace("  ", " ")
                                archive_content = archive_content.split(" ")

                                for i in range(0, len(archive_content)):
                                    if archive_content[i] == "":
                                        del archive_content[i]

                                with col2:
                                    with st.expander(label="Conteudo", expanded=True):

                                        display_content = ""
                                        for i in range(0, len(archive_content)):
                                            display_content += str(archive_content[i]) + "\n\n"
                                        
                                        st.code(display_content)

                        elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                st.error(body="A senha informada é inválida.")

                        elif safe_password != confirm_safe_password:
                            with col2:
                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                st.error(body="As senhas informadas não coincidem.")

                    elif consult_button and confirm_selection == False:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.warning(body="Confirme a seleção dos dados.")

            elif user_archives_quantity == 0:
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.warning(body="Você ainda não possui arquivos registrados.")

        def update_archive():

            user_archives_quantity = query_executor.simple_consult_query(search_user_archives_quantity, params=(logged_user_name, logged_user_document))
            user_archives_quantity = query_executor.treat_simple_result(user_archives_quantity, to_remove_list)
            user_archives_quantity = int(user_archives_quantity)

            if user_archives_quantity >= 1:

                col1, col2 = st.columns(2)

                archives_names = []
                user_archives_name = query_executor.complex_consult_query(search_user_archives_name, params=(logged_user_name, logged_user_document))
                user_archives_name = query_executor.treat_numerous_simple_result(user_archives_name, to_remove_list)

                for i in range(0, len(user_archives_name)):
                    archives_names.append(user_archives_name[i])

                with col1:

                    with st.expander(label="Consulta", expanded=True):
                        selected_archive = st.selectbox(label="Selecione o arquivo", options=archives_names)
                        safe_password = st.text_input(label="Informe sua senha", type="password")
                        confirm_safe_password = st.text_input(label="Confirme sua senha", type="password")
                        confirm_selection = st.checkbox(label="Confirmar dados", value=False)

                        if confirm_selection:

                            is_password_valid, hashed_password = user.check_login(logged_user, safe_password)

                            if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:

                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                    
                                archive_content_query = """
                                SELECT
                                    arquivo_texto.nome_arquivo,
                                    arquivo_texto.conteudo
                                FROM
                                    arquivo_texto
                                INNER JOIN
                                    usuarios ON arquivo_texto.usuario_associado = usuarios.nome
                                AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
                                WHERE
                                    arquivo_texto.nome_arquivo = %s
                                AND
                                arquivo_texto.usuario_associado = %s
                                AND arquivo_texto.documento_usuario_associado = %s;
                                """

                                archive_content = (query_executor.complex_compund_query(query=archive_content_query, list_quantity=2, params=(selected_archive, logged_user_name, logged_user_document) ))
                                archive_content = (query_executor.treat_complex_result(archive_content, to_remove_archive_list))

                                for i in range(0, len(archive_content)):
                                    if archive_content[i] == "":
                                        del archive_content[i]

                                with col1:
                                    with st.expander(label="Conteudo", expanded=True):

                                        display_content = ""
                                        for i in range(0, len(archive_content)):
                                            display_content += str(archive_content[i]) + "\n\n"
                                        
                                        st.code(display_content)
                                
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(0.5)

                                    with st.expander(label="Novos dados", expanded=True):
                                        new_archive_name = st.text_input(label="Novo nome do arquivo", max_chars=100, help="É necessário definir um nome para identificação e consulta posterior.")
                                        new_uploaded_file = st.file_uploader(label="Escolha um arquivo de texto", type=["txt"], help="São permitidos arquivos de texto, na extensão '.txt'. O tamanho do arquivo não pode exceder 200 MB.")
                                        confirm_new_data = st.checkbox(label="Confirmar novos dados")

                                        content = None

                                        if new_uploaded_file:
                                            content = new_uploaded_file.read().decode("utf-8")
                                            with col2:
                                                with st.spinner(text="Carregando arquivo..."):
                                                    sleep(0.5)
                                                if content != "":
                                                    with st.expander(label="Conteudo do arquivo carregado", expanded=True):
                                                        st.info(content)
                                                elif content == "":
                                                    with col2:
                                                        st.error(body="O Conteudo do arquivo está vazio.")
                                        
                                    update_archive_button = st.button(label=":arrows_counterclockwise: Atualizar arquivo")

                                if confirm_new_data and update_archive_button:

                                    with st.spinner(text="Aguarde..."):
                                        sleep(2.5)

                                    if new_archive_name != "" and content is not None:
                                        archive_query = "INSERT INTO arquivo_texto (nome_arquivo, conteudo, usuario_associado, documento_usuario_associado) VALUES (%s, %s, %s, %s)"
                                        archive_values = (new_archive_name,content,logged_user_name,logged_user_document)

                                        if content is not None:

                                            query_executor.insert_query(archive_query, archive_values, "Upload do arquivo realizado com sucesso!", "Erro ao fazer upload do arquivo:")

                                            log_query = """INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)"""
                                            log_query_values = (logged_user, "Atualização", "Atualizou os dados do arquivo {}.".format(new_archive_name))
                                            query_executor.insert_query(log_query, log_query_values, "Log gravado.", "Erro ao gravar log:")

                            elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(0.5)
                                    st.error(body="A senha informada é ínválida.")

                            if safe_password != confirm_safe_password:
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(0.5)
                                    st.error(body="As senhas informadas não coincidem.")

            elif user_archives_quantity == 0:
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.warning(body="Você ainda não possui arquivos registrados.")

        def delete_archive():
            user_archives_quantity = query_executor.simple_consult_query(search_user_archives_quantity, params=(logged_user_name, logged_user_document))
            user_archives_quantity = query_executor.treat_simple_result(user_archives_quantity, to_remove_list)
            user_archives_quantity = int(user_archives_quantity)

            if user_archives_quantity >= 1:

                col1, col2 = st.columns(2)

                archives_names = []
                user_archives_name = query_executor.complex_consult_query(search_user_archives_name, params=(logged_user_name, logged_user_document))
                user_archives_name = query_executor.treat_numerous_simple_result(user_archives_name, to_remove_list)

                for i in range(0, len(user_archives_name)):
                    archives_names.append(user_archives_name[i])

                with col1:

                    with st.expander(label="Consulta", expanded=True):
                        selected_archive = st.selectbox(label="Selecione o arquivo", options=archives_names)
                        safe_password = st.text_input(label="Informe sua senha", type="password")
                        confirm_safe_password = st.text_input(label="Confirme sua senha", type="password")
                        confirm_selection = st.checkbox(label="Confirmar dados", value=False)

                        if confirm_selection:

                            is_password_valid, hashed_password = user.check_login(logged_user, safe_password)

                            if safe_password != "" and confirm_safe_password != "" and confirm_safe_password == safe_password and is_password_valid == True:

                                with st.spinner(text="Aguarde..."):
                                    sleep(0.5)
                                    
                                archive_content_query = """
                                SELECT
                                    arquivo_texto.nome_arquivo,
                                    arquivo_texto.conteudo
                                FROM
                                    arquivo_texto
                                INNER JOIN
                                    usuarios ON arquivo_texto.usuario_associado = usuarios.nome
                                AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
                                WHERE
                                    arquivo_texto.nome_arquivo = %s
                                AND
                                    arquivo_texto.usuario_associado = %s
                                    AND arquivo_texto.documento_usuario_associado = %s;
                                """

                                archive_content = (query_executor.complex_compund_query(query=archive_content_query, list_quantity=2, params=(selected_archive, logged_user_name, logged_user_document) ))
                                archive_content = (query_executor.treat_complex_result(archive_content, to_remove_archive_list))

                                for i in range(0, len(archive_content)):
                                    if archive_content[i] == "":
                                        del archive_content[i]

                                with col2:
                                    with st.expander(label="Conteudo", expanded=True):

                                        display_content = ""
                                        for i in range(0, len(archive_content)):
                                            if "\\n" in archive_content[i]:
                                                display_content = str(archive_content[i])
                                                display_content = display_content.replace("\\n", " ")
                                            else:
                                                display_content += str(archive_content[i]) + "\n\n"
                                        
                                        st.code(display_content)                                    
                                        confirm_data_deletion = st.checkbox(label="Confirmar exclusão dos dados")
                                        
                                    delete_archive_button = st.button(label=":wastebasket: Deletar arquivo")

                                if confirm_data_deletion and delete_archive_button:
                                    
                                    with col2:
                                        with st.spinner(text="Aguarde..."):
                                            sleep(2.5)
                                        
                                        delete_archive_query = '''
                                        DELETE arquivo_texto FROM arquivo_texto
                                        INNER JOIN
                                            usuarios ON arquivo_texto.usuario_associado = usuarios.nome
                                        AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
                                        WHERE arquivo_texto.nome_arquivo = %s
                                        AND arquivo_texto.usuario_associado = %s
                                        AND arquivo_texto.documento_usuario_associado = %s;'''
                                        archive_values = (selected_archive, logged_user_name, logged_user_document)

                                        query_executor.insert_query(delete_archive_query, archive_values, "Arquivo deletado com sucesso!", "Erro ao deletar arquivo:")

                                        log_query = """INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)"""
                                        log_query_values = (logged_user, "Exclusão", "Excluiu o arquivo {}.".format(selected_archive))
                                        query_executor.insert_query(log_query, log_query_values, "Log gravado.", "Erro ao gravar log:")

                            elif safe_password != "" and confirm_safe_password != "" and confirm_safe_password == safe_password and is_password_valid == False:
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(0.5)
                                    st.error(body="A senha informada é inválida.")

                            elif safe_password != confirm_safe_password:
                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(0.5)
                                    st.error(body="As senhas informadas não coincidem.")

            elif user_archives_quantity == 0:
                col1, col2, col3 = st.columns(3)
                with col2:
                    with st.spinner(text="Aguarde..."):
                        sleep(0.5)
                    st.warning(body="Você ainda não possui arquivos registrados.")

        def archives_main_menu():

            col1, col2, col3 = st.columns(3)

            with col1:
                st.header(body=":spiral_note_pad: Arquivos")

            with col2:
                menu_options = ["Registrar arquivo", "Consultar arquivo", "Atualizar arquivo", "Deletar arquivo"]

                selected_option = st.selectbox(label="Menu", options=menu_options)

            st.divider()
            if selected_option == menu_options[0]:
                create_new_archive()
            elif selected_option == menu_options[1]:
                read_archive()
            elif selected_option == menu_options[2]:
                update_archive()
            elif selected_option == menu_options[3]:
                delete_archive()

        self.main_menu = archives_main_menu

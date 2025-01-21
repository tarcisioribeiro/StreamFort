from dictionary.vars import to_remove_list
from data.session_state import logged_user, logged_user_password
from functions.query_executor import QueryExecutor
import streamlit as st


name_query: str = "SELECT nome FROM usuarios WHERE login = %s AND senha = %s;"
sex_query: str = "SELECT sexo FROM usuarios WHERE login = %s; AND senha = %s;"
name_doc_query = """SELECT nome, documento_usuario FROM usuarios WHERE login = %s AND senha = %s;"""

query_executor = QueryExecutor()

user_name_doc = query_executor.complex_compund_query(query=name_doc_query, list_quantity=2, params=(logged_user, logged_user_password))
user_name_doc = query_executor.treat_numerous_simple_result(user_name_doc, to_remove_list)

logged_user_name = user_name_doc[0]
logged_user_document = user_name_doc[1]
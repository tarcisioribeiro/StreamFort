from dictionary.sql import name_doc_query
from dictionary.vars import to_remove_list
from functions.query_executor import QueryExecutor

query_executor = QueryExecutor()

user_name_doc = query_executor.complex_compund_query(query=name_doc_query, list_quantity=2, list_prefix_name='user_')
user_name_doc = query_executor.treat_numerous_simple_result(user_name_doc, to_remove_list)

logged_user_name = user_name_doc[0]
logged_user_document = user_name_doc[1]
from functions.login import Login


user_id, user_document = Login().get_user_data()
user_id = int(user_id)
user_document = str(user_document)

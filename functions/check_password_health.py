import streamlit as st

class PasswordValidator:
    def __init__(self):
        pass

    @staticmethod
    def check_password_validity(password):
        return isinstance(password, str)

    @staticmethod
    def check_password_length(password):
        length = len(password)
        if length < 4:
            return "LOW"
        elif 4 <= length <= 8:
            return "MEDIUM"
        else:
            return "STRONG"

    @staticmethod
    def check_password_strength(password):
        if not PasswordValidator.check_password_validity(password):
            return ":rotating_light: A senha deve ser composta de caracteres."

        length_rating = PasswordValidator.check_password_length(password)

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        score = sum([has_upper, has_lower, has_digit, has_special])

        if length_rating == "LOW":
            return "Muito Fraca" if score < 2 else "Fraca"
        elif length_rating == "MEDIUM":
            return "Média" if score < 3 else "Forte"
        elif length_rating == "STRONG":
            return "Forte" if score < 4 else "Muito Forte"

        return "Senha inválida."

if __name__ == "__main__":
    password_validator = PasswordValidator()
    password = st.text_input(label="Informe a senha: ", type="password")
    confirm_button = st.button(label="Confirmar")
    if confirm_button:
        strength = password_validator.check_password_strength(password)
        st.divider()
        st.info(strength)
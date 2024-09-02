import streamlit as st


class PasswordValidator:

    def __init__(self):

        def check_password_validity(password):
            if type(password).__name__ == "str":
                return True
            else:
                return False

        def check_password_length(password):

            length_avaliation = ""

            if len(password) > 0 and len(password) < 4:
                length_avaliation = "LOW"
            elif len(password) >= 4 and len(password) <= 8:
                length_avaliation = "MEDIUM"
            elif len(password) > 8:
                length_avaliation = "STRONG"

            return length_avaliation

        def check_password_complexity(password):

            valid_password = check_password_validity(password)

            password_strength_categories = {
                0: "Muito Fraca",
                1: "Fraca",
                2: "Média",
                3: "Forte",
                4: "Muito Forte",
            }

            password_strength = ""

            if valid_password == True:

                password_length_avaliation = check_password_length(password)

                capitals_ocurrence = any(c.isupper() for c in password)
                lowercases_occurrence = any(c.islower() for c in password)
                number_occurence = any(c.isdigit() for c in password)
                special_carachters_occurrence = any(not c.isalnum() for c in password)

                if (
                    password_length_avaliation == "LOW"
                    and capitals_ocurrence == False
                    and number_occurence == False
                    and lowercases_occurrence == True
                    and special_carachters_occurrence == False
                ) or (
                    password_length_avaliation == "MEDIUM"
                    and capitals_ocurrence == False
                    and number_occurence == False
                    and lowercases_occurrence == True
                    and special_carachters_occurrence == False
                ) or (
                    password_length_avaliation == "MEDIUM"
                    and capitals_ocurrence == False
                    and number_occurence == True
                    and lowercases_occurrence == False
                    and special_carachters_occurrence == False
                ):
                    password_strength = password_strength_categories[0]
                elif (
                    password_length_avaliation == "LOW"
                    and capitals_ocurrence == True
                    and number_occurence == True
                    and lowercases_occurrence == True
                    and special_carachters_occurrence == False
                ) or (
                    password_length_avaliation == "MEDIUM"
                    and capitals_ocurrence == False
                    and number_occurence == False
                    and lowercases_occurrence == True
                    and special_carachters_occurrence == False
                ):
                    password_strength = password_strength_categories[1]
                elif (
                    (
                        password_length_avaliation == "LOW"
                        and capitals_ocurrence == True
                        and lowercases_occurrence == True
                        and number_occurence == True
                        and special_carachters_occurrence == False
                    )
                    or (
                        password_length_avaliation == "MEDIUM"
                        and capitals_ocurrence == True
                        and lowercases_occurrence == True
                        and number_occurence == False
                        and special_carachters_occurrence == False
                    )
                    or (
                        password_length_avaliation == "MEDIUM"
                        and capitals_ocurrence == False
                        and lowercases_occurrence == True
                        and number_occurence == False
                        and special_carachters_occurrence == True
                    )
                    or (
                        password_length_avaliation == "MEDIUM"
                        and capitals_ocurrence == False
                        and lowercases_occurrence == True
                        and number_occurence == True
                        and special_carachters_occurrence == False
                    )
                    or (
                        password_length_avaliation == "STRONG"
                        and capitals_ocurrence == False
                        and lowercases_occurrence == True
                        and number_occurence == False
                        and special_carachters_occurrence == False
                    )
                ):
                    password_strength = password_strength_categories[2]

                elif (
                    (
                        password_length_avaliation == "LOW"
                        and capitals_ocurrence == True
                        and lowercases_occurrence == True
                        and number_occurence == True
                        and special_carachters_occurrence == True
                    )
                    or (
                        password_length_avaliation == "MEDIUM"
                        and capitals_ocurrence == True
                        and lowercases_occurrence == True
                        and number_occurence == True
                        and special_carachters_occurrence == False
                    )
                    or (
                        password_length_avaliation == "MEDIUM"
                        and capitals_ocurrence == False
                        and lowercases_occurrence == True
                        and number_occurence == True
                        and special_carachters_occurrence == True
                    )
                    or (
                        password_length_avaliation == "STRONG"
                        and capitals_ocurrence == True
                        and lowercases_occurrence == True
                        and number_occurence == False
                        and special_carachters_occurrence == False
                    )
                ):
                    password_strength = password_strength_categories[3]
                elif (
                    password_length_avaliation == "MEDIUM"
                    and capitals_ocurrence == True
                    and lowercases_occurrence == True
                    and number_occurence == True
                    and special_carachters_occurrence == True
                ) or (
                    password_length_avaliation == "STRONG"
                    and capitals_ocurrence == True
                    and lowercases_occurrence == True
                    and number_occurence == True
                    and (
                        special_carachters_occurrence == True
                        or special_carachters_occurrence == False
                    )
                ):
                    password_strength = password_strength_categories[4]
                return password_strength

            else:
                return st.error(
                    body=":rotating_light: A senha deve ser composta de caracteres."
                )

        self.check_password_strength = check_password_complexity


if __name__ == "__main__":
    password_validator = PasswordValidator()
    password = st.text_input(label="Informe a senha: ", type="password")
    confirm_button = st.button(label="Confirmar")
    if confirm_button:
        strength = password_validator.check_password_strength(password)
        st.divider()
        st.info(strength)

class PasswordValidator:
    """
    Realiza a análise da validade e força de senhas.
    """
    @staticmethod
    def check_password_validity(password):
        """
        Verifica se a senha informada é uma cadeia de caracteres.

        Parameters
        ----------
        password
            A senha a ser validada.

        Returns
        -------
        isinstance() : bool
            Retorna se a senha é ou não uma cadeia de caracteres.
        """
        return isinstance(password, str)

    @staticmethod
    def check_password_length(password):
        """
        Analisa o tamanho  da senha.

        Parameters
        ----------
        password
            A senha a ser analisada.

        Returns
        -------
        str
            O tamanho da senha (LOW, MEDIUM, STRONG).
        """
        length = len(password)
        if length < 8:
            return "LOW"
        elif 8 <= length <= 16:
            return "MEDIUM"
        else:
            return "STRONG"

    @staticmethod
    def check_password_strength(password):
        """
        Analisa a força da senha.

        Parameters
        ----------
        password
            A senha a ser analisada.

        Returns
        -------
        str
            A força da senha (Muito Fraca, Fraca, Média, Forte, Muito Forte).
        """
        if not PasswordValidator.check_password_validity(password):
            return "A senha deve ser composta de caracteres."

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

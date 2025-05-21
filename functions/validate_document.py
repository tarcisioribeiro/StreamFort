import streamlit as st


class Documents:
    """
    Classe com métodos para validação de documentos.
    """

    def validate_credit_card(self, card_number: str):
        """
        Realiza a validação do número de cartões de crédito.

        Parameters
        ----------
        card_number : str
            O número do cartão de crédito.

        Returns
        -------
        bool
            Se o cartão é válido ou inválido.
        """
        total = 0

        st.info("Validando cartão...")

        if len(card_number) != 16:
            return False

        elif len(card_number) == 16:

            if " " in card_number:
                return False

            for i in range(0, 16, 2):
                accumulated = int(card_number[i]) * 2
                if accumulated > 9:
                    accumulated = accumulated - 9
                total = total + accumulated

            for i in range(1, 17, 2):
                total = total + int(card_number[i])

            if (total % 10) != 0 or total > 150:
                return False

            return True

    def validate_owner_document(self, owner_document: str):
        """
        Realiza a validação do documento pessoal do usuário.

        Parameters
        ----------
        owner_document : str
            O número do documento pessoal.

        Returns
        -------
        bool
            Se o documento é válido ou inválido.
        """
        if len(owner_document) != 11:
            st.error(
                body="""
                O documento pessoal não tem menos e nem mais que 11 caracteres.
                """
            )
        else:
            st.info(body="Validando documento...")
            owner_document_list = []
            for i in range(0, len(owner_document)):
                owner_document_list.append(owner_document[i])

            first_counter = 10
            first_sum_value = 0

            for i in range(0, 9):
                first_sum_value += int(owner_document_list[i]) * first_counter
                first_counter = first_counter - 1

            first_division_rest = (first_sum_value * 10) % 11

            second_counter = 11
            second_sum_value = 0

            for i in range(0, 9):
                second_sum_value += int(
                    owner_document_list[i]) * second_counter
                second_counter = second_counter - 1

            second_sum_value += first_division_rest * second_counter

            second_division_rest = (second_sum_value * 10) % 11

            if first_division_rest == int(
                owner_document_list[9]
            ) and second_division_rest == int(owner_document_list[10]):
                st.success(
                    body="O documento {} é válido.".format(owner_document))
                return True
            else:
                st.error(body="O documento {} é inválido.".format(
                    owner_document
                    )
                )
                return False

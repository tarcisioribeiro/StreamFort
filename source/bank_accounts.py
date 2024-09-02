from dictionary.sql import check_user_bank_accounts_query
from functions.query_executor import QueryExecutor
import streamlit as st


class BankAccount:

    def __init__(self):

        def main_menu():
            @st.dialog("Cast your vote")
            def vote(item):
                st.write(f"Why is {item} your favorite?")
                reason = st.text_input("Because...")
                if st.button("Submit"):
                    st.session_state.vote = {"item": item, "reason": reason}
                    st.rerun()

            if "vote" not in st.session_state:
                st.write("Vote for your favorite")
                if st.button("A"):
                    vote("A")
                if st.button("B"):
                    vote("B")
            else:
                f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

        self.main_menu = main_menu
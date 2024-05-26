import streamlit as st
import os
from neo4j_ import valid_credentials, Neo4jCredentials

N4J_CREDS_KEY = "NEO4J_CREDS"
N4J_URI_KEY = "NEO4J_URI"
N4J_USERNAME_KEY = "NEO4J_USERNAME"
N4J_PASSWORD_KEY = "NEO4J_PASSWORD"
N4J_DATABASE_KEY = "NEO4J_DATABASE"

ENV_NEO4J_URI = os.getenv(N4J_URI_KEY, "bolt://localhost:7687")
ENV_NEO4J_USERNAME = os.getenv(N4J_USERNAME_KEY, "neo4j")
ENV_NEO4J_PASSWORD = os.getenv(N4J_PASSWORD_KEY, None)
ENV_NEO4J_DATABASE = os.getenv(N4J_DATABASE_KEY, "neo4j")


def sidebar():
    if N4J_CREDS_KEY not in st.session_state:
        st.session_state[N4J_CREDS_KEY] = Neo4jCredentials(
            uri=ENV_NEO4J_URI,
            username=ENV_NEO4J_USERNAME,
            password=ENV_NEO4J_PASSWORD,
            database=ENV_NEO4J_DATABASE,
        )

    with st.sidebar:
        st.subheader("Neo4j Config")
        uri = st.text_input("URI", st.session_state[N4J_CREDS_KEY].uri)
        username = st.text_input("Username", st.session_state[N4J_CREDS_KEY].username)
        password = st.text_input(
            "Password", st.session_state[N4J_CREDS_KEY].password, type="password"
        )
        database = st.text_input("Database", st.session_state[N4J_CREDS_KEY].database)

        if (
            uri != st.session_state[N4J_CREDS_KEY].uri
            or username != st.session_state[N4J_CREDS_KEY].username
            or password != st.session_state[N4J_CREDS_KEY].password
            or database != st.session_state[N4J_CREDS_KEY].database
        ):

            st.session_state[N4J_CREDS_KEY] = Neo4jCredentials(
                uri=uri, username=username, password=password, database=database
            )

        if st.button("Validate Credentials"):
            # Validate connection
            creds = st.session_state[N4J_CREDS_KEY]
            if valid_credentials(creds):
                st.success("Valid credentials!")
            else:
                st.error("Invalid credentials")

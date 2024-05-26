import streamlit as st
from sidebar_ import sidebar, N4J_CREDS_KEY
from code_editor import code_editor
from neo4j_ import query_db
import json

st.set_page_config(layout="wide", page_title="Neo4j Python Explorer")
sidebar()

c1, c2 = st.columns(2)
records, summary, keys = None, None, None

with c1:
    st.subheader("Cypher")

    # Load button options for streamlit-code-editor
    with open("neo4j_python_explorer/buttons.json") as json_button_file_alt:
        btns = json.load(json_button_file_alt)

    # Params
    with st.expander("Optional Parameters"):
        st.write("Click the 'Run' button within the editor to commit the parameters.")
        params = {}
        default_params = "{\n\t\n}"

        # Use editors run button to commit the params
        params_dict = code_editor(default_params, buttons=btns)
        print(f"Params: {params_dict}")
        if params_dict["type"] == "submit" and len(params_dict["text"]) != 0:
            params = json.loads(params_dict["text"])
            st.success("Parameters committed.")

    # Query
    st.write("*Click the 'Run' button within the editor to execute query*")
    default_code = """\nMATCH (n)\nRETURN n"""

    response_dict = code_editor(default_code, buttons=btns)
    print(f"response_dict: {response_dict}")

    if response_dict["type"] == "submit" and len(response_dict["text"]) != 0:

        query = response_dict["text"]
        print(f"Query: {query}")

        # Run query
        records, summary, keys = query_db(
            st.session_state[N4J_CREDS_KEY], query, params
        )


with c2:
    st.subheader("Output")
    if summary is not None:
        st.write("Summary:")
        st.code(summary)
    if keys is not None:
        st.write("Keys:")
        st.code(keys)
    if records is not None:
        with st.expander(f"{len(records)} Raw Records"):
            st.write(records)

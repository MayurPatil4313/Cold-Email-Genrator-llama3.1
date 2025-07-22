import sys
import os

# Override sqlite3 with the version from pysqlite3-binary
import pysqlite3
sys.modules["sqlite3"] = pysqlite3.dbapi2
os.environ["SQLITE_PREFER_PYSQLITE3"] = "1"

import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader
import os

from dotenv import load_dotenv
_ = load_dotenv()

# streamlit run main.py --server.port 8502

# os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "true"

def create_streamlit_app(llm , portfolio, clean_text):
    st.title(' 📩 Cold Email Generator')

    url_input = st.text_input("Enter a URL: ", value='https://careers.nike.com/lead-data-scientist/job/R-62512')
    SENDER_NAME = st.text_input("Sender Name *", placeholder='Enter your Name')
    SERVICE_ORG_NAME = st.text_input("Organization name *", placeholder='Enter organization name')
    email_length = st.number_input("Email Length*",placeholder='Enter email length in words', 
        min_value=100,
        max_value=300,
        step=1,
        value=100
    )

    submit_button = st.button('Submit')

    if submit_button:
        try:
            if SENDER_NAME.strip() == "":
                st.warning("Name is required.")
            if url_input.strip() == "":
                st.warning("URL is required.")
            if SERVICE_ORG_NAME.strip() == "":
                st.warning("Organization Name required.")

            else:   
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links,SENDER_NAME,SERVICE_ORG_NAME,email_length)
                    st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

FACT_CHECKING_APIS = {
    "snopes": "https://api.snopes.com/v1/fact-check",
    "politifact": "https://api.politifact.com/fact-check",
}

def call_fact_check_apis(news_article):
    """
    Call fact-checking APIs to verify the news article.
    
    Args:
        news_article (str): The content of the news article to fact-check.
    
    Returns:
        list: API responses with fact-checking results.
    """
    api_responses = []
    
    for api_name, api_url in FACT_CHECKING_APIS.items():
        try:
            response = requests.post(api_url, data={"query": news_article})
            if response.status_code == 200:
                api_responses.append(response.json())
            else:
                st.error(f"Error from {api_name}: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to {api_name}: {str(e)}")
    
    if not api_responses:
        st.warning("No fact-check results found.")
    
    return api_responses

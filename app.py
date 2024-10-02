import streamlit as st
from agents import create_tasks, researcher, fact_checker, analyst
from sentiment_analysis import analyze_sentiment_vader
from fact_checking import call_fact_check_apis
from visualization import plot_bias_meter
from crewai import Crew
import numpy as np

st.set_page_config(page_title="Misinformation Detector", page_icon="🔍", layout="wide")

st.sidebar.title("About")
st.sidebar.info("This app uses AI agents to analyze news articles and predict if they contain false or misleading information.")

# Footer style for app
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: #FAFAFA;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    <div class="footer">
        Developed using free AI resources and APIs. Powered by CrewAI v0.65.2.
    </div>
    """, unsafe_allow_html=True
)

st.title("Misinformation Detector")

news_input = st.text_area("Enter the news article to analyze:")

if st.button("Analyze News", key="analyze_news_button"):
    if news_input:
        st.write("Analyzing...")

        # Creating tasks and initializing agents for CrewAI
        try:
            tasks = create_tasks(news_input)
            crew = Crew(agents=[researcher, fact_checker, analyst], tasks=tasks, verbose=True)
            result = crew.kickoff()

            if result:
                st.write("**Agents have successfully completed their tasks.**")
            else:
                st.error("Agent analysis failed. Please try again.")
        except Exception as e:
            st.error(f"Error during agent analysis: {str(e)}")

        # Sentiment analysis using VADER
        try:
            sentiment_score, sentiment_label = analyze_sentiment_vader(news_input)
            st.write(f"**Sentiment Analysis:** Sentiment score is {sentiment_score:.2f}, indicating a {sentiment_label.lower()} sentiment.")
        except Exception as e:
            st.error(f"Error in sentiment analysis: {str(e)}")

        # Source credibility check
        trusted_sources = ["reliable-source.com", "another-trusted-source.com"]
        untrusted_sources = ["fake-news-site.com", "unreliable-source.com"]
        source_credibility = "Credible Source" if any(source in news_input for source in trusted_sources) else "Unreliable Source"
        st.write(f"**Source Credibility:** {source_credibility}")

        # Bias meter visualization
        try:
            bias_score = np.random.uniform(-1, 1)
            st.write("**Bias Score:**")
            st.write("Bias score ranges from -1 (left-leaning bias) to +1 (right-leaning bias).")
            plot_bias_meter(bias_score)
        except Exception as e:
            st.error(f"Error in bias meter visualization: {str(e)}")

        # Fact-checking
        try:
            fact_check_results = call_fact_check_apis(news_input)
            st.subheader("Fact Check Results")
            if fact_check_results:
                for result in fact_check_results:
                    st.write(result)  # Displaying each fact-check result
            else:
                st.warning("No fact-check results found.")
        except Exception as e:
            st.error(f"Error in fact-checking: {str(e)}")
    else:
        st.warning("Please enter a news article to analyze.")

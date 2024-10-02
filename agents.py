import os
import logging
from crewai import Crew, Agent, Task
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
        temperature=0, 
        groq_api_key=os.getenv("GROQ_API_KEY"), 
        model_name="mixtral-8x7b-32768"
    )

search_tool = DuckDuckGoSearchRun()

try:
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Conduct in-depth research to find relevant and factual information about the claims in the news article.",
        backstory=(
            "As a Senior Research Analyst with over 15 years of experience, you specialize in political news, "
            "international relations, and current events. You have an exceptional ability to sift through large volumes "
            "of information across diverse news outlets, identifying patterns, trends, and potential misinformation. "
            "Your expertise lies in navigating complex datasets and drawing meaningful insights that provide a well-rounded "
            "and unbiased view of any news topic. Your approach is highly analytical, methodical, and guided by rigorous "
            "standards of accuracy and reliability."
        ),
        tools=[search_tool],
        llm=model
    )

    fact_checker = Agent(
        role="Veteran Fact Checker",
        goal="Scrutinize the accuracy of the claims made in the news article by verifying against trusted sources.",
        backstory=(
            "With over 20 years of experience as a seasoned journalist and fact-checker, you have worked with top-tier "
            "media organizations to verify facts and uphold journalistic integrity. Your role involves cross-referencing "
            "information with verified databases, publications, and independent sources to ensure the utmost accuracy. "
            "Known for your meticulous attention to detail, you possess a deep understanding of media ethics, fact-checking "
            "protocols, and the ability to distinguish between factual reporting and false claims. Your experience has made "
            "you an authority in identifying manipulated or misleading content in political and general news."
        ),
        tools=[search_tool],
        llm=model
    )

    analyst = Agent(
        role="Expert Political Analyst",
        goal="Evaluate the news article for potential bias, inaccuracies, and hidden agendas.",
        backstory=(
            "As a highly regarded political analyst with a PhD in Political Science, you have spent over two decades analyzing "
            "geopolitical events, policy decisions, and media bias. Your deep expertise in global political dynamics, media bias, "
            "and the influence of political agendas on news reporting makes you uniquely qualified to dissect news content. "
            "You have an innate ability to detect subtle biases, assess the context behind media portrayals, and provide a nuanced "
            "understanding of how current events are framed. Your analysis is respected for its depth, objectivity, and clarity, "
            "making you a trusted source in the world of political commentary."
        ),
        llm=model
    )
except Exception as e:
    logging.error(f"Error initializing agents: {e}")
    raise


def create_tasks(news_article):
    """
    Create a list of tasks for analyzing the given news article.
    
    Args:
        news_article (str): The content of the news article to analyze.
    
    Returns:
        list of Task: A list of tasks to be executed by the AI agents.
    """
    logging.info("Creating tasks for the article analysis...")

    if not news_article or not isinstance(news_article, str):
        logging.error("News article content is empty or not a valid string.")
        raise ValueError("News article content cannot be empty and must be a string.")
    
    try:
        tasks = [
            Task(
                description="Conduct a comprehensive research on the main claims and entities mentioned in the news article. Focus on identifying credible sources and relevant patterns across different news outlets.",
                agent=researcher,
                expected_output="A detailed and well-researched report highlighting the main claims, key entities, and any patterns found in the article."
            ),
            Task(
                description="Perform a rigorous fact-check of the claims in the article, cross-referencing against authoritative databases and trusted news sources.",
                agent=fact_checker,
                expected_output="A fact-checked report that lists the claims from the article, stating which are verified as accurate, debunked, or need further clarification."
            ),
            Task(
                description="Analyze the article for any potential political bias, misinformation, or misleading narratives. Provide insights on how the framing of the information aligns or conflicts with international political contexts.",
                agent=analyst,
                expected_output="A comprehensive political analysis, identifying any bias, misleading content, and providing an objective evaluation of how the article fits within the wider geopolitical landscape."
            )
        ]
        
        logging.info(f"Successfully created {len(tasks)} tasks for analysis.")
        return tasks
    except Exception as e:
        logging.error(f"Error while creating tasks: {e}")
        raise


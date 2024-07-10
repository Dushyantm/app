# sql_agent.py
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

def create_sql_agent_executor():
    db = SQLDatabase.from_uri("sqlite:///./database/travel_database.db")
    
    agent_executor = create_sql_agent(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
        db=db,
        agent_type="openai-tools",
        verbose=True
    )
    
    return agent_executor

sql_agent_executor = create_sql_agent_executor()

def execute_sql_query(query: str):
    try:
        result = sql_agent_executor.invoke(query)
        return result
    except Exception as e:
        raise Exception(f"Error executing SQL query: {str(e)}")
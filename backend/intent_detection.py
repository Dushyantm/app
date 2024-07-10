from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

class IntentDetection:
    def __init__(self, query):
        self.query = query

    def detect_intent(self):
        template = '''
        Detect the intent of the query. 
        The schema for the SQL database is:
        -- Travel Agents
CREATE TABLE travel_agents (
    agent_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    website TEXT
);

-- Destinations
CREATE TABLE destinations (
    destination_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    description TEXT
);

-- Travel Packages
CREATE TABLE travel_packages (
    package_id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    destination_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    duration_days INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES travel_agents (agent_id),
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id)
);

        Return if the query requires data from the SQL database or should be executed by the general LLM agent.
        Responses:
        1. SQL
        2. LLM

        Query: {query}

        Just mention the response and nothing else.
'''
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        intent_prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )
        intent_chain = intent_prompt | llm
        response = intent_chain.invoke(self.query)
        print(response.content)  # Print the response
        return response.content.strip().upper()

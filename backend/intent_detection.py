from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

class IntentDetection:
    def __init__(self, query):
        self.query = query

    def detect_intent(self):
        template = '''
Determine the Intent of User Queries for Database Interaction

Database Schema Overview:

1. Travel Agents Table
Stores data about travel agents, including an identifier, name, email, phone number, and website.
Schema:

CREATE TABLE travel_agents (
    agent_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    website TEXT
);
2. Destinations Table
Contains information about travel destinations such as an identifier, name, country, and description.
Schema:

CREATE TABLE destinations (
    destination_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    description TEXT
);
3. Travel Packages Table
Holds records of travel packages, linked to travel agents and destinations. Includes details like package name, description, duration, and price.
Schema:

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
Query Intent Detection:

Decide whether a user's query pertains to extracting or manipulating data from the described SQL database, 
or if it should be handled by a general Language Learning Model (LLM) for non-database-related tasks.

Possible Responses:
1. SQL
2. LLM

Example:
User Query: "I want to book a flight to boston can you help me with some travel agents details"
Intent: SQL

User Query: "What is the distance from Boston to Qubec?"
Intent: LLM

User Query: {query}
Intent: 
'''
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        intent_prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )
        intent_chain = intent_prompt | llm
        response = intent_chain.invoke(self.query)
        # print(response.content)  # Print the response
        return response.content.strip().upper()

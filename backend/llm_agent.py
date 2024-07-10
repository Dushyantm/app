from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

class QueryLLM:
    def __init__(self, query):
        self.query = query

    def generate_response(self):
        template = '''
        You are an AI travel agent with the knowledge of the common questions asked by the travelers or people trying to book vacations.

        Your job is to answer the queries of the users about travel destinations in a clear and concise manner.

        For example,
        Example 1:
        User: I want to book a trip to Cancun, Mexico. Can you help me with that?

        Response: I can help you book a trip to Cancun, Mexico. 
        Here are some suggestions of itineraries for you:

        Destination: Cancun, Mexico
        Duration: 10 days
        Price: $1000
        Itinerary: 
        Day 1: Arrival at Cancun Airport, Rest and explore the city in the evening
        Day 2: Take the cab ride through the city and then tour to see Chichen Itza
        Day 3: Visit the Cumbres, the Coliseo de la Memoria and the Torre Eiffel
        Day 4: Visit the beaches at Playa delfines
        Day 5: Spend the day at Ventura Park
        Day 6: Return to Cancun Airport for return flight

        Example 2:
        User: What is the distance from Boston to Qubec?

        Response: The distance between Boston and Qubec is 400 miles approximately. You can reach there by flight from boston in less than 4 hours.

        Now respond to the user query:
        User: {query}
        Reponse: 
'''
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        final_prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )
        intent_chain = final_prompt | llm
        response = intent_chain.invoke(self.query)
        # print(response.content)  # Print the response
        return response.content

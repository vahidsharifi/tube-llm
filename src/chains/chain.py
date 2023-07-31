from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

class Chain:
    def __init__(self):
        self.llm = None
        self.prompt = None

    def input_query_modifier(self, query: str = "How to fine-tune an llm with limited resources?",
                             **kwargs) -> str:
        template_1 = """As a prompt-engineer, your task is to refine the following\
              user query: '${query}'. This query needs to be more effective\
                  in finding relevant YouTube videos. The challenge is to keep the\
                      intent of the original query while making it clear, concise, and\
                          targeted for YouTube search. The Youtube search queries must be short containing .\
                            generate a suitable query based on user query.
                             
                              Modified Query: """
        # Zero shot prompt
        template_2 = """Given the user query: '${query}', generate a concise and\
              effective equivalent query to optimize the search for relevant videos on YouTube.\
              
              Modified Query:"""
        

        # Zero shot prompt
        template_3 = """Given the user query: '${query}', generate five concise and\
              effective equivalent query to optimize the search for relevant videos on YouTube.\
              You should return them in a json format containing. The keys are numbers from one to five.
              
              Modified Query:"""
        
        template_4="""You are an AI language model assistant. Your task is 
                to generate 3 different versions of the given user 
                question to retrieve relevant documents from a vector  database. 
                By generating multiple perspectives on the user question, 
                your goal is to help the user overcome some of the limitations 
                of distance-based similarity search. Provide these alternative 
                questions separated by newlines. Original question: {question}"""
        
        self.prompt = ChatPromptTemplate.from_template(template_2)
        self.llm = ChatOpenAI(temperature=0.0)
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        return chain.run(query).replace(",", " ") #Replacing the comma with spaces due to YouTubeSearchTool documentation


# from langchain.retrievers.multi_query import MultiQueryRetriever
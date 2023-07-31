from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

class Chain:
    def __init__(self):
        self.llm = None
        self.prompt = None

    def input_query_modifier(self, query: str = "How to fine-tune an llm with limited resources?",
                             **kwargs):
        template_1 = """As a prompt-engineer, my task is to refine the following\
              user query: '${query}'. This query needs to be more effective\
                  in finding relevant YouTube videos. The challenge is to keep the\
                      intent of the original query while making it clear, concise, and\
                          targeted for YouTube search. How would I modify this query?"""

        template_2 = """Given the user query: '${query}', generate a concise and\
              effective equivalent query to optimize the search for relevant videos on YouTube\.
              
              Modified Query:"""
        self.prompt = ChatPromptTemplate.from_template(template_2)
        self.llm = ChatOpenAI(temperature=0.0)
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        return chain.run(query)

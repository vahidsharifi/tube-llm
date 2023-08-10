from langchain.tools import DuckDuckGoSearchResults
import ast

class Tools:

    def __init__(self):
        pass

    def duckduckgo_search(self, query: str = "How to fine-tune LLamA-2?", num_results: int = 4,
                          **kwargs):
        search = DuckDuckGoSearchResults(num_results=num_results)
        result = search.run(query)
        return result




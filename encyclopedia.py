import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

class Encyclopedia:
    '''A class responsible for handling non-specific commands to the assistant'''

    AMBIGUITY_ERROR_MESSAGE = "Result was too ambiguious to summarize"
    SUMMARY_ERROR = "An error encountered while trying to summarize a response"

    def __init__(self):
        self._result_page = None

    def search(self, query, limit=4):
        '''This method takes a query to be searched on wikipedia'''

        return wikipedia.search(query, results=limit)

    def summarize(self, article_title, limit=2):
        '''Takes a specific article title and summarizes the result limiting it to
        the specfied number of sentences'''

        article_summary = ""
        try:
            article_summary = wikipedia.summary(article_title, sentences=limit)
        except DisambiguationError:
            article_summary = self.AMBIGUITY_ERROR_MESSAGE
        except Exception:
            article_summary = self.SUMMARY_ERROR

        return article_summary
    
    def set_result_page(self, the_result): 
        '''Creates and sets the web page object for the passed search result. If no page exists
        for the specified page, nothing is set'''
        
        try:
            self._result_page = wikipedia.page(the_result)
        except PageError:
            self._result_page = None

    def get_result_page(self):
        '''Returns the result web page object'''

        return self._result_page
    
    def get_result_url(self):
        '''Retrieves the result page's url if it exist'''

        return self._result_page.url if self._result_page != None else "No URL exists"



if __name__ == "__main__":
    info_db = Encyclopedia()
    search_results = info_db.search(input("Query>> "))
    print(search_results)
    selected_result = search_results[0]
    print(selected_result)
    info_db.set_result_page(selected_result)
    print(info_db.summarize(selected_result))
    print(info_db.get_result_url())



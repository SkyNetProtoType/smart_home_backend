from todoist import TodoistAPI
from decouple import config

API_KEY = config("TODOIST_API_KEY")

class TodoistService:

    def __init__(self) -> None:
        '''Intiializes connection to the Todoist application'''
        self._api = TodoistAPI(API_KEY)
        self._api.sync()

    
    def getProjects(self):
        '''Retrieves all the projects/list-group from Todoist'''
        return self._api.state['projects']

    
    def getItems(self):
        '''Retrieves all the individual tasks (in every project) from Todoist'''
        return self._api.state['items']


    def addItemToProject(self, item_name: str, proj_id: int) :
        '''Adds a specific item to a project based on the project Id'''
        self._api.items.add(item_name, project_id=proj_id)
        self._api.commit()


    def findById(self, search_list, obj_id):
        '''Finds a specific object in a list'''
        target = None
        for obj in search_list:
            if obj['id'] == obj_id:
                target = obj
                break
        return target


    def findProjectById(self, proj_id: int):
       '''Finds a specific project on Todoist'''
       projects = self.getProjects()
       return self.findById(search_list=projects, obj_id=proj_id)


    def findItemById(self, item_id: int):
        '''Finds a specific task item on todoist'''
        items = self.getItems()
        return self.findById(search_list=items, obj_id=item_id)
    
   

if __name__ == "__main__":
    from product import load_products
    shopping_list_id = 2276166027
    # service = TodoistService()
    # for product in load_products()[:2]:
    #     service.addItemToProject(product['name'], shopping_list_id)
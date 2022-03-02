from typing import List
from pprint import pprint
from todoist import TodoistAPI
from todoist.models import Item
from decouple import config

API_KEY = config("TODOIST_API_KEY")

class TodoistService:
    '''API information can be found here:
        https://todoist-python.readthedocs.io/en/latest/todoist.html
        https://todoist-python.readthedocs.io/en/latest/_modules/todoist/models.html#Model
    '''

    def __init__(self) -> None:
        '''Intiializes connection to the Todoist application'''
        self._api = TodoistAPI(API_KEY)
        self._api.sync()

    
    def getProjects(self):
        '''Retrieves all the projects/list-group from Todoist'''
        return self._api.state['projects']

    
    def getItems(self):
        '''Retrieves all the task items (in every project) from Todoist'''
        return self._api.state['items']


    def addItemToProject(self, item_name: str, proj_id: int) :
        '''Adds a specific task item to a project based on the project Id'''
        self._api.items.add(item_name, project_id=proj_id)
        self._api.commit()
    

    def addItemsToProject(self, items: List[str], project_id: int):
        for item in items:
            self._api.items.add(item)
        self._api.commit()


    def findById(self, search_list, obj_id):
        '''Finds a specific object in a list. search_list can be Items, Projects etc.'''
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


    def findItemById(self, item_id: int) -> Item:
        '''Finds a specific task item (i.e. irrespective of the parent project)'''
        items = self.getItems()
        return self.findById(search_list=items, obj_id=item_id)


    def findItemsByProjectById(self, project_id: int) -> List[Item]:
        '''Finds a list of task item under a specific project. e.g. all the tasks under "shopping list" '''
        project_items = []
        items = self.getItems()
        for item in items:
            if item['project_id'] == project_id:
                project_items.append(item)
        return project_items


    def deleteItemById(self, item_id: int) -> None:
        '''Deletes a specific task item (i.e. irrespective of the parent project)'''
        try:
            item_to_delete = self.findItemById(item_id)
            item_to_delete.delete()
            self._api.commit()
        except Exception as e:
            print(e)

    def markAllItemsCompleteForProject(self, projectId: int):
        '''Marks only task items under a specific project as complete. This ensures that you do not mark other task items'''
        items_to_process = self.findItemsByProjectById(project_id=projectId)
        processed_items = items_to_process.copy() #hold a copy of the items before processing
        for item in items_to_process:
            item.complete()
        self._api.commit()
        return processed_items
    
    def markAllItemsDeletedForProject(self, projectId: int):
        '''Marks only task items under a specific project as deleted. This ensures that you do not mark other task items'''
        items_to_delete = self.findItemsByProjectById(project_id=projectId)
        deleted_items = items_to_delete.copy() #hold a copy of the items before processing
        for item in items_to_delete:
            item.delete()
        self._api.commit()
        return deleted_items


    def processQueueItems(self, queue_id) -> List[Item]:
        '''Marks all the task items in the queue as deleted and returns the processed items'''
        queue_items = self.markAllItemsDeletedForProject(queue_id)
        return [item['content'] for item in queue_items] #only the name of the task item



   

if __name__ == "__main__":
    from product import load_products
    shopping_list_id = 2276166027
    queue_id = 2285886894
    service = TodoistService()

    #--------------------Populating Items in different projects--------------------------
    # service.addItemsToProject([product['name'] for product in load_products()[:3]] , shopping_list_id)
    # service.addItemsToProject(['test item1', 'test item2', 'test item 3'], queue_id)

    #--------------------Locating Items in different projects--------------------------
    # shopping_list_items = service.findItemsByProjectById(project_id=shopping_list_id)
    # print("Shopping List =", [item['content'] for item in shopping_list_items])
    queue_items = service.findItemsByProjectById(project_id=queue_id)
    print("Queue products =", [item['content'] for item in queue_items])

    #--------------------Process queue products--------------------------
    # print(service.processQueueItems(queue_id))
    
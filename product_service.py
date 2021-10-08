from typing import List
from product_repository import ProductRepository
import os

class ProductService:
    '''Service class that performs business logic relating to products'''

    CURRENT_DIR = os.path.dirname(__file__)
    DB_SRC = os.path.join(CURRENT_DIR, 'db', "smarthome.db")

    @staticmethod
    def get_products():
        '''Retrieves all the products from the database and converts them
        to a JSON before returning it to the controller'''
        connection = ProductRepository.connect_to_database(ProductService.DB_SRC)
        result_set =  ProductRepository.retrieve_all(connection)
        return ProductService.convert_to_json_list(result_set)


    @staticmethod
    def update_product(product):
        '''Updates a specific product in the database.'''
        connection = ProductRepository.connect_to_database(ProductService.DB_SRC)
        ProductRepository.update(product, connection)

    
    @staticmethod
    def convert_to_json_list(result_set: List[tuple]):
        '''Converts the result set from the database (i.e. a list of
        tuples) into a list of dicts/JSONs with the appropriate keys'''
        products_as_json:List[dict] = []

        for tuple in result_set:
            product_json = {}
            product_json['id'] = tuple[0]
            product_json['name'] = tuple[1]
            product_json['category'] = tuple[2]
            product_json['quantity'] = tuple[3]
            product_json['addedToCart'] = True if tuple[4] == 1 else False
            products_as_json.append(product_json)
        
        return products_as_json
from typing import List
from product_repository import ProductRepository
from datetime import datetime
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
    def get_cart_products():
        '''Retrieves all the cart items from the database'''
        connection = ProductRepository.connect_to_database(ProductService.DB_SRC)
        result_set =  ProductRepository.retrieve_cart_items(connection)
        return ProductService.convert_to_json_list(result_set)

    @staticmethod
    def add_new_product(product):
        '''Adds a new product to the database'''
        connection = ProductRepository.connect_to_database(ProductService.DB_SRC)
        ProductRepository.insert(product, connection)

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
            id, name, category, quantity, cart_status = tuple
            product_json = {}
            product_json['id'] = id
            product_json['name'] = name
            product_json['category'] = category
            product_json['quantity'] = quantity
            product_json['addedToCart'] = True if cart_status == 1 else False
            products_as_json.append(product_json)
        
        return products_as_json

    
    @staticmethod
    def convert_product_to_str(products: List[dict]): 
        '''Formats a list of products as a string with only their names'''

        final_string = f"Shopping list for {datetime.now():%m-%d-%Y}\n"
        final_string += "================================\n"
        for bulleting, product in enumerate(products, 1):
            final_string += f"{bulleting}. {product['name']}\n"
        
        return final_string
        



if __name__ == "__main__":
    cart_products = [{'name':'fries'},{'name':'bread'},{'name':'banana'}]
    print(ProductService.convert_product_to_str(cart_products))
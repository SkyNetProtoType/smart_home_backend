from typing import List
from product_repository import ProductRepository
import os

class ProductService:
    CURRENT_DIR = os.path.dirname(__file__)
    DB_SRC = os.path.join(CURRENT_DIR, 'db', "smarthome.db")

    @staticmethod
    def get_products():
        connection = ProductRepository.connect_to_database(ProductService.DB_SRC)
        result_set =  ProductRepository.retrieve_all(connection)
        return ProductService.convert_to_json_list(result_set)

    @staticmethod
    def convert_to_json_list(result_set: List[tuple]):
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


    @staticmethod
    def update_product(product):
        connection = ProductRepository.connect_to_database(ProductService.DB_SRC)
        ProductRepository.update(product, connection)
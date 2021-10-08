
import sqlite3
from typing import List
from sqlite3 import Error, Connection

class ProductRepository:
    CREATE_PRODUCTS_TABLE = '''CREATE TABLE IF NOT EXISTS products
          (id INTEGER PRIMARY KEY,
           name TEXT,
           category TEXT,
           quantity INT,
           addedToCart INT);
           '''
    INSERT_PRODUCTS = '''INSERT INTO products (id, name, category, quantity, addedToCart)
            VALUES(?,?,?,?,?)
            '''
    
    UPDATE_PRODUCT = '''UPDATE products
            SET quantity=?, addedToCart=?
            WHERE id = ?'''
    
    SELECT_PRODUCT = '''SELECT id, name, category, quantity, addedToCart
            FROM products
            WhERE id = ?
            '''
    DELETE_ALL_PRODUCTS = '''DELETE FROM products'''
    
    SELECT_ALL_PRODUCTS = '''SELECT * FROM products'''


    @staticmethod
    def connect_to_database(db_name: str) -> Connection:
        '''Establishes a connection to the database. Error message is
        printed out if the application faills to connect.'''

        connection = None
        try:
            connection = sqlite3.connect(db_name)
        except Error as e:
            print('Connection Error: ' + str(e) )

        return connection
    
    @staticmethod
    def create_table(conn: Connection):
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.CREATE_PRODUCTS_TABLE)
        except Error as e:
            print('Create Table Error: '+ str(e))

    
    @staticmethod
    def insert(product: dict, conn:Connection) -> int:
        '''Inserts a task object into the tasks table. Returns the id
        of the row inserted'''

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.INSERT_PRODUCTS, (int(product['id']), product['name'], 
                product['category'], product['quantity'], product['addedToCart']))
            conn.commit()
        except Error as e:
            print ('Insertion Error: '+ str(e))

        return cursor.lastrowid

    @staticmethod
    def update(product: dict, conn: Connection):
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.UPDATE_PRODUCT, (product['quantity'], product['addedToCart'],
            product['id']))
            conn.commit()
        except Error as e:
            print ('Update Error: '+ str(e))


    @staticmethod
    def delete_all(conn: Connection):
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.DELETE_ALL_PRODUCTS)
            conn.commit()
        except Error as e:
            print ('Delete Error: '+ str(e))

    
    @staticmethod
    def retrieve_all(conn: Connection) -> List[tuple]:
        '''Retrieves all of the tasks in the task table'''

        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.SELECT_ALL_PRODUCTS)
        except Error as e:
            print(e)
        
        return cursor.fetchall()
    

if __name__ == "__main__":
    import os
    from product import load_products

    #establishing the path to the database
    current_dir = os.path.dirname(__file__)
    db_source = os.path.join(current_dir, 'db', "smarthome.db")
    print(db_source) 
    conn = ProductRepository.connect_to_database(db_source)

    #performing test on database
    if conn is not None:
        # ProductRepository.create_table(conn) #ignores creating a table if it exists
        # id, name, category, qty, addedToCart = input("Enter <id>, <name>, <category>, <qty>, <cartstatus: 0 or 1>: ").split(', ')
        # product = { 'name': name,
        #             'category': category,
        #             'quantity': int(qty),
        #             'addedToCart': addedToCart,
        #             'id' : id,
        #         }
        # product_id = ProductRepository.insert(product, conn)
        # print('Product Id:', product_id)
       
        # product2 = { 'name': name,
        #             'category': category,
        #             'quantity': int(qty),
        #             'addedToCart': addedToCart,
        #             'id' : id,
        #         }
        # ProductRepository.update(product2, conn)

        # PRELOADING DATA
        # preloaded_products = load_products()
        # for product in preloaded_products:
        #     ProductRepository.insert(product, conn)

        # ProductRepository.delete_all(conn)
        print(ProductRepository.retrieve_all(conn))
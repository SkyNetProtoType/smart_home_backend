import sqlite3
from typing import List
from sqlite3 import Error, Connection

class ProductRepository:
    '''A class that performs CRUD operations on the products table in
    smarthome.db'''

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
            SET quantity=?, addedToCart=?, category=?
            WHERE id = ?'''
    
    SELECT_PRODUCT = '''SELECT id, name, category, quantity, addedToCart
            FROM products
            WhERE id = ?
            '''
    SELECT_ALL_PRODUCTS = '''SELECT * FROM products ORDER BY name'''

    SELECT_CART_PRODUCTS = '''SELECT * FROM products WHERE addedToCart=1 ORDER BY name'''

    DELETE_PRODUCT = '''DELETE FROM products WHERE id=?'''

    DELETE_ALL_PRODUCTS = '''DELETE FROM products'''
    

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
        '''Creates the product table if it doesn't exist'''
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.CREATE_PRODUCTS_TABLE)
        except Error as e:
            print('Create Table Error: '+ str(e))


    @staticmethod
    def insert(product: dict, conn:Connection) -> int:
        '''Inserts a product into the products table. Returns the id
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
    def retrieve(conn: Connection, id) -> List[tuple]:
        '''Retrieves all of the products in the product table'''

        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.SELECT_PRODUCT, (id,))
        except Error as e:
            print(e)
        
        return cursor.fetchall()
    
    @staticmethod
    def retrieve_all(conn: Connection) -> List[tuple]:
        '''Retrieves all of the products in the product table'''

        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.SELECT_ALL_PRODUCTS)
        except Error as e:
            print(e)
        
        return cursor.fetchall()

    @staticmethod
    def retrieve_cart_items(conn: Connection) -> List[tuple]:
        '''Retrieves all of the products in the product table that are in the cart'''

        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.SELECT_CART_PRODUCTS)
        except Error as e:
            print(e)
        
        return cursor.fetchall()


    @staticmethod
    def update(product: dict, conn: Connection):
        '''Updates a specific product in the database '''
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.UPDATE_PRODUCT, (product['quantity'], product['addedToCart'],
            product['category'], product['id']))
            conn.commit()
        except Error as e:
            print ('Update Error: '+ str(e))


    @staticmethod
    def delete(conn: Connection, id):
        '''Delete a product in the product table'''
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.DELETE_PRODUCT, (id,))
            conn.commit()
        except Error as e:
            print ('Delete Error: '+ str(e))


    @staticmethod
    def delete_all(conn: Connection):
        '''Deletes all the rows in the product table'''
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(ProductRepository.DELETE_ALL_PRODUCTS)
            conn.commit()
        except Error as e:
            print ('Delete Error: '+ str(e))

    

if __name__ == "__main__":
    import os

    #establishing the path to the database
    current_dir = os.path.dirname(__file__)
    db_source = os.path.join(current_dir, 'db', "smarthome.db")
    print(db_source) 
    conn = ProductRepository.connect_to_database(db_source)

    #------PERFORMING VARIOUS CRUD TESTS ON THE DATABASE-----
    if conn is not None:
        # ProductRepository.create_table(conn) #ignores creating a table if it exists
        
        #-------RECEIVE USER INPUT AND INSERT INTO DATABASE-----
        # id = int(input("Enter next id number after last item in the table: "))
        # while True:
        #     name, category = input("Enter <name>, <category>: ").split(', ')
        #     product = { 'name': name,
        #                 'category': category.capitalize(),
        #                 'quantity': 1,
        #                 'addedToCart': 0,
        #                 'id' : id,
        #             }
        #     id+=1
        #     product_id = ProductRepository.insert(product, conn)
        #     print('Product Id:', product_id)
       
        #------UPDATE A SPECIFIC PRODUCT IN THE DATABASE-------
        # product2 = { 'name': name,
        #             'category': category,
        #             'quantity': int(qty),
        #             'addedToCart': addedToCart,
        #             'id' : id,
        #         }
        # ProductRepository.update(product2, conn)

        #-------PRELOADING DATA INTO THE DATABASE---------
        # preloaded_products = load_products()
        # for product in preloaded_products:
        #     ProductRepository.insert(product, conn)

        # ProductRepository.delete_all(conn)
        # print(ProductRepository.retrieve_all(conn))
        print(ProductRepository.retrieve(conn, "10"))
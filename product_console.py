import os
from product_repository import ProductRepository
from product_service import ProductService
from prettytable import PrettyTable

class ProductConsole:

    def __init__(self) -> None:
        current_dir = os.path.dirname(__file__)
        db_source = os.path.join(current_dir, 'db', "smarthome.db")

        self._conn = ProductRepository.connect_to_database(db_source)

    def retrieve_product(self) -> dict:
        '''Asks for the product Id and retrieves the specific product'''

        id = input("Product Id: ")
        product = ProductService.convert_to_json_list(
                ProductRepository.retrieve(self._conn, id))
        return product[0]


    def show_all_products(self):
        '''Shows all the products in the products table'''

        table = PrettyTable()
        table.field_names = ["Id", "Name", "Category", "Qty", "Added to Cart"]
        products = ProductRepository.retrieve_all(self._conn)
        table.add_rows(products)
        print(table)
        

    def show_specific_product(self):
        '''Shows a specific product'''

        print(self.retrieve_product())


    def insert_product(self):
        '''Inserts a specific product into the table'''

        id = int(input("Enter next id number after last item in the table: "))
        num_products = int(input("Number of products to insert: "))
        for i in range(num_products):
            name, category = input("Enter <name>, <category>: ").split(", ")
            product = { 'name': name,
                        'category': category.capitalize(),
                        'quantity': 1,
                        'addedToCart': 0,
                        'id' : id,
                        }
            id+=1
            product_id = ProductRepository.insert(product, self._conn)
            print('Product Id:', product_id)
        
   
    def update_category(self):
        product = self.retrieve_product()
        new_category = input("Enter the new category: ").capitalize()
        product['category'] = new_category
        ProductRepository.update(product, self._conn)
        print("Update successful for id: ", product['id'])
    
    def delete_product(self):
        product = self.retrieve_product()
        ProductRepository.delete(self._conn, product['id'])
        print("Delete successful for id: ", product['id'])



if __name__ == "__main__":
    console = ProductConsole()

    print("Product Database Console\n========================")
    menu_options = "1. Show all products\n2. Show a product\n3. Insert product\n4. Update category\n5. Delete product\n\n Enter 'q' to quit\n"
    print("Choose an option:")
    print(menu_options)
    choice = input("Option: ")
    while choice != 'q':
        if choice == "1":
            console.show_all_products()
        elif choice == "2":
            console.show_specific_product()
        elif choice == "3":
            console.insert_product()
        elif choice ==  "4":
            console.update_category()
        elif choice == "5":
            console.delete_product()
        else:
            print("Choose an option on the menu or Enter 'q'")
        
        print("\n\nChoose an option:")
        print(menu_options)
        choice = input("Option: ")


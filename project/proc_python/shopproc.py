
from dataclasses import dataclass, field
from typing import List
import csv
import os.path
import sys

@dataclass
class Product:
    name: str = ""
    price: float = 0.00

@dataclass 
class ProductStock:
    product: Product
    quantity: int

@dataclass 
class Shop:
    cash: float = 0.00
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.00
    shopping_list: List[ProductStock] = field(default_factory=list)


def print_product(p):
    print(f'PRODUCT NAME: {p.name} \nPRODUCT PRICE: €%.2f' % (p.price))
    return p.name, p.price

def create_and_stock_shop(file_path):
    s = Shop()
    fileexists =  os.path.exists(file_path)
    if fileexists == False:
        print("\nShop File not found, Exit program")
        sys.exit()
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
           
    return s

def print_shop(s):
    print(f'\n\n*******************')
    print(f'Shop has €%.2f in cash' % (s.cash))
    print(f'******************')
    for item in s.stock:
        print(f'\nThe shop has %0.0f of:' % (item.quantity))
        print_product(item.product)
        print(f'-------------')

def read_customer(file_path):

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            c = Customer(first_row[0], float(first_row[1]))
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = ProductStock(p, quantity)
                c.shopping_list.append(ps)
            return c 

def print_customer(c, s):
    print(f'=============== Order ================\n\n')
    print(f'The Order is from  {c.name} and with a budget of:  €%.2f' % (c.budget))
    print(f'-------------\n')

    total = 0
    
    # Test for Quantity
    quan = 0
    
    # List for Shop and Customer Products
    custlist = []
    shoplist = []
    
    # Loop through customer products
    for citem in c.shopping_list:
        cusItem = citem.product.name
        cusQuan = int(citem.quantity)

        # Add to customer product list
        custlist.append(cusItem)
                
        # Loop through shop products
        for sitem in s.stock:
            shopItem  = sitem.product.name
            shopItemPrice = sitem.product.price

            # If shop and customer products match
            if shopItem == cusItem:
                
                # Get subtotal 
                subtotal = round((shopItemPrice * cusQuan),2)
                # Add to shop product list
                shoplist.append(shopItem)
                if (sitem.quantity >= citem.quantity):

                    total = total + subtotal

                elif (sitem.quantity < citem.quantity):
                    print(f"The shop cannot fill the order of product: {cusItem}\n")
                    quan = 1
            
    outofstock = set(custlist) - set(shoplist)
   
    if (quan == 1):
        print(f"\n-------------\n")
        print(f"Unfortunately the shop cannot fill you order\n")
        print(f"------------\n\n")
        return

    elif (c.budget < total):
        insufficient_funds = total - c.budget
        print(f"\n-------------")
        print(f"The total cost of {c.name} shopping is €%.2f" % (total))
        print(f"{c.name} requires €%.2f more for the shopping"% (insufficient_funds))
        print(f"------------")
        return


    elif (c.budget >= total ):

        for citem in c.shopping_list:
            cusItem = citem.product.name
            cusQuan = int(citem.quantity)
        
        
            for sitem in s.stock:
                shopItem  = sitem.product.name
                shopItemPrice = sitem.product.price
                

                if shopItem == cusItem:
                    sitem.quantity = sitem.quantity - citem.quantity
                    print(f'The cost of {shopItem} in the shop is €%.2f' % (shopItemPrice))
                    subtotal = round((shopItemPrice * cusQuan),2)
                    print(f'The cost of {cusQuan} {cusItem} in the shop is €%.2f\n' % subtotal)

        for oos in outofstock:
            print(f"Sorry the following item is out of stock: {oos}")


        s.cash = s.cash + total
  
        print(f"\n-------------")
        print(f'The total cost of {c.name} shopping is €%.2f' % (total))

        change = c.budget - total
        print(f'You have change of €%.2f' % (change))
        print(f"------------\n")
        
        shopcash = shop.cash + total
        print(f"\n-------------")
        print(f'The shop balance is now %.2f\n' , shopcash)
       

        change = self.budget - total
        print(f'The total cost of {self.name} shopping is €%.2f\n' % (total))
        print(f'{self.name} has change of €%.2f' % (change))
        print(f"------------\n")


def makeAnOrder():
    orderName  = input("Please Enter Your Name : ")
    orderBudget  = input("Please Enter your Budget: ")
    
    print("Your name is : {} and you have €{}".format(orderName, orderBudget))
    customer = Customer(orderName, float(orderBudget))
    ProdList = int(input("How many products do you have on your Shopping List: "))

    i = 0

    while i < ProdList:

        pname = input("\nWhat Product do you Require? ")

        quantity = float(input("How many of {} do you require? ".format(pname)))

        p = Product(pname)
        ps = ProductStock(p, quantity)
        customer.shopping_list.append(ps)

        print(f'The product is: {pname} and you want %.0f ' % (quantity))

        i += 1

    return customer

def main():

    s = create_and_stock_shop('../stock.csv')

    while True: 
        display_menu()
        userchoice = input("Enter your choice :  ")

        if (userchoice == "1"):
            print_shop(s)

        elif (userchoice == "2"): 
            c = makeAnOrder()
            print_customer(c, s)

        elif (userchoice == "3"): 
            selectedfile = input("What file would you like to view? ")
            filepath = str("../" + selectedfile)
            fileexists = os.path.exists(filepath)
            c = read_customer(filepath)
            print_customer(c, s)

        elif (userchoice == "4"): 
            print("\nTHANKS FOR SHOPPING!\n")
            exit(1)
            break
        
        else:
            print("\nOooops, Incorrect value entered. Please try again or click 4 to exit\n")

def display_menu():
    print("======================================================\n")
    print("                Welcome To the Fruit Shop             \n")
    print("======================================================\n")
    print("                     1. View Stock                   \n")
    print("                     2. Make an Order                \n")
    print("                     3. View Order from File         \n")
    print("                     4. Exit                         \n")
    print("======================================================\n")


if __name__ == "__main__":
    main()
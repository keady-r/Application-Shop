import csv
import time
#Setting Classes
class Product:
    
    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
class ProductStock:
    
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    def name(self):
        return self.product.name
    
    def unit_price(self):
        return self.product.price
        
    def cost(self):
        return self.unit_price() * self.quantity
        
class Shop:
    
    def __init__(self, path):
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
                
    def print_shop(self):
        print(f'\n\n==========================')
        print(f'At the start of the day the Shop has €%.2f in cash' % (self.cash))
        print(f'=============================\n')
        for item in self.stock:
            print(f'-------------')
            print(f'\n We have  %.2f of the following item:' % (item.quantity))
            print(f'PRODUCT: {item.product.name} \n PRICE: €%.2f' % (item.product.price))
            print(f'-------------')

class Customer:

    def __init__(self, path):
        self.shopping_list = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps) 
#This will take in the name of the order and the budget.
    def print_customer(self):
        print(f'=============== Order ================\n\n')
        print(f'The Order is from  {self.name} with a budget of:  €%.2f' % (self.budget))
        print(f'-------------\n')
#This will check the order against the quantity in the store
    def inventorycheck(orderlist, inventorylist):
        outofstock = set(orderlist) - set(inventorylist)
        for oos in outofstock:
            print(f"Sorry the following item is out of stock: {oos}")

    def calculate_costs(self, shop):

        amount = 0
        total = 0

        orderlist = []
        inventorylist = []
                
        for shop_item in shop.stock:
            inventorylist.append(shop_item.product.name)

            for list_item in self.shopping_list:
                orderlist.append(list_item.name())

                if (list_item.name() == shop_item.name()):

                    subtotal = round((shop_item.product.price * list_item.quantity),2)

                    if (shop_item.quantity >= list_item.quantity):
                        total = total + subtotal

                    elif (shop_item.quantity < list_item.quantity):
                        print(f"Apologies We cannot complete the order, no stock for: {list_item.name()}\n")
                        amount = 1



        if (amount == 1):
            print(f"\n______________________________________________\n")
            print(f"|                                              |\n")
            print(f"|    Out of Stock - Order cannot be complete   |\n")
            print(f"|______________________________________________|\n\n")
            return

        elif (self.budget < total):
            insufficient_funds = total - self.budget
            print(f"\n-------------")
            print(f"The total cost of {self.name} shopping is €%.2f" % (total))
            print(f"{self.name} requires €%.2f more for the shopping"% (insufficient_funds))
            print(f"------------")
            return

        elif (self.budget >= total ):

            for shop_item in shop.stock:
            
                for list_item in self.shopping_list:

                    if (list_item.name() == shop_item.name()):
                        cusQuan = int(list_item.quantity)
                        
                        shop_item.quantity = shop_item.quantity - list_item.quantity

                        print(f'The cost of {shop_item.product.name} in the shop is €%.2f' % (shop_item.product.price))
                        subtotal = round((shop_item.product.price * list_item.quantity),2)
                        print(f'The cost of {cusQuan} {shop_item.product.name} in the shop is €%.2f\n' % subtotal)
            
        Customer.inventorycheck(orderlist, inventorylist)
        
#Update the store cashflow following successful purchase 
        shopcash = shop.cash + total
        print(f'The total cost of {self.name} shopping is €%.2f\n' % (total))
        print(f"\n-------------")
        print(f'The shop balance is now {shopcash}\n\n')
        print(f"------------\n")

    
    def makeAnOrder():
        
        orderName  = input("Please Enter Your Name : ")
        orderBudget  = input("Please Enter your Budget: ")
        print("Your name is : {} and you have €{}".format(orderName , orderBudget ))
        customer = Customer(orderName, orderBudget)
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

    s = Shop("../stock.csv")

    while True: 
        display_menu()

        userchoice = input("Enter your choice :  ")

        if (userchoice == "1"):
            Shop.print_shop(s)

        elif (userchoice == "2"): 
            customer = Customer(orderName, orderBudget)
            Customer.print_customer(customer)
            
        elif (userchoice == "3"): 
            selectedfile = input("What file would you like to view? ")
            filepath = str("../" + selectedfile)
            customer = Customer(filepath)
            Customer.print_customer(customer)
            customer.calculate_costs(s)

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
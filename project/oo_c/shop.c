//Author Ruth Keady
//Submission for assessment - MultiParadigm. ATU 2022
// Shop creation in C


// This code was developed from a template shop created as part of the lecture content. References will be given throughout the code were appropriate. 

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Product {
	char* name; 						
	double price;  							
};

struct ProductStock {						
	struct Product product;					
	int quantity;							
};

struct Shop {
	double cash;  						
	struct ProductStock stock[20];			
	int index;								
};

struct Customer {
	char* custname; 							
	double budget; 							
	struct ProductStock shoppingList[10];	
	int index;								
};

//Reference - Lecture Material, print out product information
void printProduct(struct Product p)
{
	printf("PRODUCT NAME: %s \nPRODUCT PRICE: €%.2f\n", p.name, p.price);
}

//Reference - Lecture Material
struct Shop createAndStockShop(const char* str)
{
    
	FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen(str, "r");
	if (fp == NULL)
        exit(EXIT_FAILURE);
	read = getline(&line, &len, fp);
	float cash = atof(line);

	struct Shop shop = { cash };

    while ((read = getline(&line, &len, fp)) != -1) {
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");

		int quantity = atoi(q);
		
		double price = atof(p);
		char *name = malloc(sizeof(char) * 50);
		strcpy(name, n);
		struct Product product = { name, price };
		struct ProductStock stockItem = { product, quantity };
		shop.stock[shop.index++] = stockItem;

    }
	
	return shop;
}

//Reference - Lecture Material
void printShop(struct Shop* s)
{
	printf("\n\n==========================\n");
	printf("At the start of the day the Shop has €%.2f in cash\n", s->cash); //adding pointer Reference: https://www.geeksforgeeks.org/arrow-operator-in-c-c-with-examples/
	printf("==========================\n");

	for (int i = 0; i < s->index; i++)
	{
		printf("\n We have  %d of the following item:\n", s->stock[i].quantity);
		printProduct(s->stock[i].product);
		printf("-------------\n");
	}
}
//Repeating same structure as Shop. Reference - Lecture Material 
struct Customer customer_file(const char* str)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen(str, "r");
    if (fp == NULL)
        {
		printf("\nFile not found, Exit program\n");	
        exit(EXIT_FAILURE);
		}

	read = getline(&line, &len, fp);
	char *cn = strtok(line, ",");
	char *custname = malloc(sizeof(char) * 50);
	strcpy(custname, cn);

	float budget = atof(strtok(NULL, ","));
	
	struct Customer custlist = { custname, budget };

    while ((read = getline(&line, &len, fp)) != -1) {
		char *n = strtok(line, ",");
		char *q = strtok(NULL, ",");
		int quantity = atoi(q);

		char *pname = malloc(sizeof(char) * 50);
		strcpy(pname, n);
		struct Product product = { pname };
		struct ProductStock stockItem = { product, quantity };
		custlist.shoppingList[custlist.index++] = stockItem;

    }
	return custlist;
}

//Reference - Lecture Material
void printCustomer(struct Customer c, struct Shop* s)
{
	printf("\n\n=============== Order ================\n\n");
	printf("The Order is from  %s with a budget of: €%.2f\n", c.custname, c.budget);
	printf("-------------\n\n");

	double total = 0;
	int quantity = 0;

//References: https://www.w3schools.com/c/c_conditions.php, 	
	for (int a = 0; a < c.index; a++)
	{
		int response = 0;
		char *orderItem = c.shoppingList[a].product.name;
	
		for (int b = 0; b < s->index; b++)
			{
				if (strcmp(s->stock[b].product.name, orderItem ) == 0)
				{
					response = 1;	
					double subtotal = c.shoppingList[a].quantity * s->stock[b].product.price;
					if (s->stock[b].quantity >= c.shoppingList[a].quantity)
					{					
						total = total + subtotal;
					}

					else if (s->stock[b].quantity == 0)
					{
						response = 2;
					}

					else if (s->stock[b].quantity < c.shoppingList[a].quantity)
					{
						response = 3;
					}
					
				}		

			}

			if (response == 2)
					{
							printf("Sorry the following item is out of stock: %s\n", orderItem);
							quantity = 1;					
					}
			else if (response == 3)
					{
							printf("The shop cannot fill the order of product: %s\n", orderItem);
							quantity = 1;
					}
	}

	if(quantity == 1)
	{
		printf("\n______________________________________________\n");
		printf("|                                              |\n");
		printf("|    Out of Stock - Order cannot be complete   |\n");
		printf("|______________________________________________|\n\n");
	}

	else if (c.budget < total){
		double insufficient_funds = total - c.budget;
		printf("\n-------------\n");
		printf("The total cost of %s shopping is €%.2f\n", c.custname, total);
		printf("%s requires %.2f more for the shopping\n", c.custname, insufficient_funds);
		printf("------------\n\n");

	}

	else if (c.budget >= total ){

		for (int a = 0; a < c.index; a++)
	{

		int response = 0;
		char *orderItem = c.shoppingList[a].product.name;
		for (int b = 0; b < s->index; b++)
			{
				if (strcmp(s->stock[b].product.name, orderItem ) == 0)
				{
					response = 1;
					s->stock[b].quantity =  s->stock[b].quantity - c.shoppingList[a].quantity;
					double subtotal = c.shoppingList[a].quantity * s->stock[b].product.price;
					printf("The cost of %s in the shop is €%.2f\n", c.shoppingList[a].product.name, s->stock[b].product.price);
					printf("The cost of %d %s in the shop is €%.2f\n\n", c.shoppingList[a].quantity, c.shoppingList[a].product.name, subtotal);

				}		

			}

			if (response == 0)
					{
							printf("Sorry the following item is not in store:%s\n", orderItem);
					}
	}	

//Update the store cashflow following successful purchase. 
		s->cash = s->cash + total;
		printf("\n-------------\n");
		printf("The total cost of %s shopping is €%.2f\n", c.custname, total);
		printf("\n-------------\n");
		printf("\n The shop balance is now €%.2f\n", s->cash);
		printf("\n-------------\n");

	}
	

}

struct Customer makeAnOrder(){
	
	char *name = malloc(sizeof(char) * 50);
	printf("Please Enter Your Name : "); 
	fgets(name, sizeof name, stdin);
  	scanf("%[^\n]%*c",name);

	float budget;
	printf("Please Enter your Budget: ");
    scanf("%f", &budget);

	printf("Hi: %s , you have €%.2f to spend\n", name, budget); 
	
	struct Customer custlist2 = { name, budget };

	int i;
	int a = 0; 
	printf("How many products do you have on your Basket?: ");
    scanf("%d", &i);
	

	do
	{
		char *pname = malloc(sizeof(char) * 50);
		printf("\nWhat Product would you like to add to your basket? "); 
		fgets(pname, sizeof pname, stdin);
  		scanf("%[^\n]%*c",pname);

		int quantity;
		printf("How many of %s do you require? ", pname);
		scanf("%d", &quantity);

		printf("The product is: %s and you want %d\n", pname, quantity); 
		a++;

		struct Product product = { pname };
		struct ProductStock stockItem = { product, quantity };
		custlist2.shoppingList[custlist2.index++] = stockItem;

	} while (a < i);
	
	return custlist2;
    
}

char * filename(){
	
	char *filename = malloc(sizeof(char) * 50);
	printf("Please Enter Filename: "); 
	fgets(filename, sizeof filename, stdin);
	scanf("%s",filename);
	const char* path = "../";
	char* filepath;
	filepath = malloc(sizeof(char) * 50); 
	strcpy(filepath, path); 
	strcat(filepath, filename); 
	return strdup(filepath);
    
}

// Reference : Shopping Cart Application in C https://www.youtube.com/watch?v=muFe2YsN1BA
int main()
{
    int userchoice, num, i;
    unsigned long int fact;

	struct Shop shop = createAndStockShop("../stock.csv");
	struct Shop* currentShopStock = &shop;

    while(1)
    {
		printf("======================================================\n");
		printf("                Welcome To the Fruit Shop             \n");
		printf("======================================================\n");
		printf("                     1. View Stock                   \n");
		printf("                     2. Make an Order                \n");
		printf("                     3. View Order from File         \n");
		printf("                     4. Exit                         \n");
		printf("======================================================\n");
		printf("\nPlease select a number from the list\n");
        scanf("%d",&userchoice);
        //Reference: https://www.programiz.com/c-programming/c-switch-case-statement
        switch(userchoice)
        {
            case 1:
                {
				printShop(currentShopStock);
				}
                break;
        
            case 2:
				{
				struct Customer shoppinglist2 = makeAnOrder();
				printCustomer(shoppinglist2, currentShopStock);
				}
				break;
			
			case 3:
				{
				char* selectedfile = filename();
				struct Customer shoppinglist = customer_file(selectedfile);
				printCustomer(shoppinglist, currentShopStock);
				}
				break;
        
            case 4:
                printf("\nTHANKS FOR SHOPPING!\n");
                exit(0);  
        }
    }
    return 0;
}

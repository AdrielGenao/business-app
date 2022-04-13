from tkinter.constants import INSERT
import pandas as pd
import csv
import tkinter as tk
from tkinter import scrolledtext
import time

purchasing=[]

class Products():
    def __init__(self):
        self.products_df = pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Products.csv", header=0)  # Make Dataframe
        self.products = self.products_df[['Name','SKU','Price A','Price B','Price C','Price D']].values  # Dataframe to numpy 2d array (w/o titles)
        self.products = self.products.tolist()  # Numpy array to regualar array (Only going to be used for editing)
        super().__init__()            
    
    def productsHome(self):
        self.productsNewScreen()
        self.buttonAdd=tk.Button(text="Add Product",font=("Arial",25),width=100,height=200,command=lambda: self.productsAddEntry())
        self.buttonAdd.grid(row=0,column=0)
        self.buttonEdit=tk.Button(text="Edit Product",font=("Arial",25),width=100,height=200,command=lambda: self.productsEditChoice())
        self.buttonEdit.grid(row=0,column=1)
        self.buttonDelete=tk.Button(text="Delete Product",font=("Arial",25),width=100,height=200,command=lambda: self.productsDelete())
        self.buttonDelete.grid(row=1,column=0)
        self.buttonView=tk.Button(text="View Products",font=("Arial",25),width=100,height=200,command=lambda: self.productsView())
        self.buttonView.grid(row=1,column=1)
        self.buttonBack=tk.Button(text="Home",font=("Arial",25),width=100,height=200,command=lambda: self.Return())
        self.buttonBack.grid(columnspan=2)

    def productsAddEntry(self): 
        self.productsNewScreen()
        self.addAskName=tk.Label(text="Name:",font=("Arial",20),width=50,height=50)
        self.addAskName.grid(row=0,column=0)
        self.addGetName=tk.Entry(font=("Arial",20))
        self.addGetName.grid(row=0,column=1)
        self.addAskSKU=tk.Label(text="SKU:",font=("Arial",20),width=50,height=50)
        self.addAskSKU.grid(row=1,column=0)
        self.addGetSKU=tk.Entry(font=("Arial",20))
        self.addGetSKU.grid(row=1,column=1)
        self.addAskPriceA=tk.Label(text="Price A:",font=("Arial",20),width=50,height=50)
        self.addAskPriceA.grid(row=2,column=0)
        self.addGetPriceA=tk.Entry(font=("Arial",20))
        self.addGetPriceA.grid(row=2,column=1)
        self.addAskPriceB=tk.Label(text="Price B:",font=("Arial",20),width=50,height=50)
        self.addAskPriceB.grid(row=3,column=0)
        self.addGetPriceB=tk.Entry(font=("Arial",20))
        self.addGetPriceB.grid(row=3,column=1)
        self.addAskPriceC=tk.Label(text="Price C:",font=("Arial",20),width=50,height=50)
        self.addAskPriceC.grid(row=4,column=0)
        self.addGetPriceC=tk.Entry(font=("Arial",20))
        self.addGetPriceC.grid(row=4,column=1)
        self.addAskPriceD=tk.Label(text="Price: D",font=("Arial",20),width=50,height=50)
        self.addAskPriceD.grid(row=5,column=0)
        self.addGetPriceD=tk.Entry(font=("Arial",20))
        self.addGetPriceD.grid(row=5,column=1)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=50, command=lambda: self.productsHome())
        self.back.grid(row=6,column=0)           
        self.ProductsConfirm=tk.Button(text="Confirm",font=("Arial",20),width=50,height=50, command=lambda: self.productsAdd())
        self.ProductsConfirm.grid(row=6,column=1)      

    def productsAdd(self):
        newRow = [self.addGetName.get(), self.addGetSKU.get(), self.addGetPriceA.get(), self.addGetPriceB.get(), self.addGetPriceC.get(), self.addGetPriceD.get()]  # Make row for the array
        self.products.append(newRow)  # Append row to array
        self.productsConfirm()  # Save changes and update dataframe
        time.sleep(1)  # Pause to show user that product is being saved to file        


    def productsEditChoice(self):
        self.productsNewScreen()
        self.productsDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))  # Text box for products display
        self.productsDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.productsHome())
        self.back.grid(column=0,row=1)   
        self.productsDisplay.insert(tk.INSERT,self.products_df.to_string(columns=['Name','SKU'],justify="right",col_space=25))  # Printing names and SKU's of products
        self.productChoose=tk.Label(text="Enter Product Row Number",font=("Arial",20),width=50,height=1)
        self.productChoose.grid(column=1,row=0)
        self.productEnter=tk.Entry(font=("Arial",20))
        self.productEnter.grid(column=1,row=0,rowspan=2)
        self.productButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.productsEdit())
        self.productButton.grid(column=1,row=1,rowspan=2)

    def productsEdit(self):    
        self.opt=int(self.productEnter.get())  # Row of product to edit
        self.productsNewScreen()
        if self.opt>=len(self.products) or self.opt<0:  # If Entry was out of bounds for products
            self.productsEditChoice()  # Reset page
        else:
            choice=self.products[self.opt]
            self.editAskName=tk.Label(text="Name:",font=("Arial",20),width=50,height=50)
            self.editAskName.grid(row=0,column=0)
            self.editGetName=tk.Entry(font=("Arial",20))
            self.editGetName.grid(row=0,column=1)
            self.editGetName.insert(tk.INSERT,choice[0])
            self.editAskSKU=tk.Label(text="SKU:",font=("Arial",20),width=50,height=50)
            self.editAskSKU.grid(row=1,column=0)
            self.editGetSKU=tk.Entry(font=("Arial",20))
            self.editGetSKU.grid(row=1,column=1)
            self.editGetSKU.insert(tk.INSERT,choice[1])
            self.editAskPriceA=tk.Label(text="Price A:",font=("Arial",20),width=50,height=50)
            self.editAskPriceA.grid(row=2,column=0)
            self.editGetPriceA=tk.Entry(font=("Arial",20))
            self.editGetPriceA.grid(row=2,column=1)
            self.editGetPriceA.insert(tk.INSERT,choice[2])
            self.editAskPriceB=tk.Label(text="Price B:",font=("Arial",20),width=50,height=50)
            self.editAskPriceB.grid(row=3,column=0)
            self.editGetPriceB=tk.Entry(font=("Arial",20))
            self.editGetPriceB.grid(row=3,column=1)
            self.editGetPriceB.insert(tk.INSERT,choice[3])
            self.editAskPriceC=tk.Label(text="Price C:",font=("Arial",20),width=50,height=50)
            self.editAskPriceC.grid(row=4,column=0)
            self.editGetPriceC=tk.Entry(font=("Arial",20))
            self.editGetPriceC.grid(row=4,column=1)
            self.editGetPriceC.insert(tk.INSERT,choice[4])
            self.editAskPriceD=tk.Label(text="Price: D",font=("Arial",20),width=50,height=50)
            self.editAskPriceD.grid(row=5,column=0)
            self.editGetPriceD=tk.Entry(font=("Arial",20))
            self.editGetPriceD.grid(row=5,column=1)
            self.editGetPriceD.insert(tk.INSERT,choice[5])
            self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=50, command=lambda: self.productsEditChoice())
            self.back.grid(row=6,column=0)           
            self.confirm=tk.Button(text="Confirm",font=("Arial",20),width=50,height=50, command=lambda: self.productsEditSave())
            self.confirm.grid(row=6,column=1)      

    def productsEditSave(self):
        self.products[self.opt]=[self.editGetName.get(), self.editGetSKU.get(), self.editGetPriceA.get(), self.editGetPriceB.get(), self.editGetPriceC.get(), self.editGetPriceD.get()]  # Row of newly edited product
        self.productsConfirm()
        time.sleep(1)  # Pause screen t show user that the product is being saved

    def productsView(self):
        self.productsNewScreen()
        self.productsDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.productsDisplay.grid(columnspan=5,row=0)
        self.productsDisplay.insert(tk.INSERT,self.products_df.to_string(justify="right",col_space=25))
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.productsHome())
        self.back.grid(row=1,columnspan=5)  
        
    def productsDelete(self):
        self.productsNewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.productsHome())
        self.back.grid(column=0,row=1)   
        self.deleteDisplay.insert(tk.INSERT,self.products_df.to_string(columns=['Name','SKU'],justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Product Row Number",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.productsDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)
    
    def productsDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())  # Row of product to delete
        if deleteRow>=len(self.products) or deleteRow<0:  # If entry was out of bounds of product list
            self.productsDelete()  # Reset page
        else:
            self.products.pop(deleteRow)  # Delete row from list of products
            self.productsConfirm()  # Save and reset dataframe and list of products
            self.productsDelete()   # Refresh page to reset textbox of products
        time.sleep(1)  # Pause page to show user that product is being deleted            
    
    def productsConfirm(self):
        with open(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Products.csv", 'w') as csvfile:  # File as written mode
            csvwriter = csv.writer(csvfile)  # Create csv writing function
            self.products.insert(0,['Name','SKU','Price A','Price B','Price C','Price D'])  # Putting titles back in to rewrite csv file correctly
            rows=0
            while rows < len(self.products):
                csvwriter.writerow(self.products[rows])  # Rewrite 2d array back into file
                rows += 1
        self.products_df = pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Products.csv", header=0)  # Updating dataframe
        self.products.pop(0)  # Taking out titles from array to be back to original array of just products

    def productsNewScreen(self):
        for widgets in window.winfo_children():
            widgets.destroy()  # Delete all widgets on page to create new one

    def Return(self):
        self.productsNewScreen()
        run=GUI()



class Customers:
    def __init__(self):
        self.customers_df=pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Customers.csv", header=0)  # Dataframe
        self.customers=self.customers_df[['Name','Email','Address']].values  # Dataframe to numpy array (w/o titles)
        self.customers=self.customers.tolist()  # Numpy array to regular list
        super().__init__()    
        
    def customersHome(self):
        self.customersNewScreen()
        self.buttonAdd=tk.Button(text="Add Customer",font=("Arial",25),width=100,height=200,command=lambda: self.customersAddEntry())
        self.buttonAdd.grid(row=0,column=0)
        self.buttonEdit=tk.Button(text="Edit Customer",font=("Arial",25),width=100,height=200,command=lambda: self.customersEditEntry())
        self.buttonEdit.grid(row=0,column=1)
        self.buttonDelete=tk.Button(text="Delete Customer",font=("Arial",25),width=100,height=200,command=lambda: self.customersDelete())
        self.buttonDelete.grid(row=1,column=0)
        self.buttonView=tk.Button(text="View Customers",font=("Arial",25),width=100,height=200,command=lambda: self.customersView())
        self.buttonView.grid(row=1,column=1)
        self.buttonBack=tk.Button(text="Home",font=("Arial",25),width=100,height=200,command=lambda: self.Return())
        self.buttonBack.grid(columnspan=2)
    
    def customersAddEntry(self):
        self.customersNewScreen()
        self.CustomersAddAskName=tk.Label(text="Name:",font=("Arial",20),width=50,height=50)
        self.CustomersAddAskName.grid(row=0,column=0)
        self.CustomersAddGetName=tk.Entry(font=("Arial",20))
        self.CustomersAddGetName.grid(row=0,column=1)
        self.addAskEmail=tk.Label(text="Email:",font=("Arial",20),width=50,height=50)
        self.addAskEmail.grid(row=1,column=0)
        self.addGetEmail=tk.Entry(font=("Arial",20))
        self.addGetEmail.grid(row=1,column=1)
        self.addAskAddress=tk.Label(text="Address:",font=("Arial",20),width=50,height=50)
        self.addAskAddress.grid(row=5,column=0)
        self.addGetAddress=tk.Entry(font=("Arial",20))
        self.addGetAddress.grid(row=5,column=1)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=50, command=lambda: self.customersHome())
        self.back.grid(row=6,column=0)           
        self.CustomersConfirm=tk.Button(text="Confirm",font=("Arial",20),width=50,height=50, command=lambda: self.customersAddSave())
        self.CustomersConfirm.grid(row=6,column=1)   

    def customersAddSave(self):
        self.customers.append([self.CustomersAddGetName.get(), self.addGetEmail.get(), self.addGetAddress.get()])  # Append row to array
        self.customersConfirm()  # Save changes and update dataframe
        time.sleep(1)  # Freeze page to show user that product is being added
          
    def customersEditEntry(self):
        self.customersNewScreen()
        self.customersDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.customersDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.customersHome())
        self.back.grid(column=0,row=1)   
        self.customersDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name','Email','Address'],justify="right",col_space=25))
        self.customerChoose=tk.Label(text="Enter Customer Row Number",font=("Arial",20),width=50,height=1)
        self.customerChoose.grid(column=1,row=0)
        self.customerEnter=tk.Entry(font=("Arial",20))
        self.customerEnter.grid(column=1,row=0,rowspan=2)
        self.customerButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.customersEdit())
        self.customerButton.grid(column=1,row=1,rowspan=2)   

    def customersEdit(self):
        self.opt=int(self.customerEnter.get())  # Get customer row number
        self.customersNewScreen()  # Clear page
        if self.opt>=len(self.customers) or self.opt<0: # If customer row number input is out of bounds 
            self.customersEditChoice()  # Reset page
        else:
            choice=self.customers[self.opt]
            self.editAskName=tk.Label(text="Name:",font=("Arial",20),width=50,height=50)
            self.editAskName.grid(row=0,column=0)
            self.editGetName=tk.Entry(font=("Arial",20))
            self.editGetName.grid(row=0,column=1)
            self.editGetName.insert(tk.INSERT,choice[0])
            self.editAskEmail=tk.Label(text="Email:",font=("Arial",20),width=50,height=50)
            self.editAskEmail.grid(row=1,column=0)
            self.editGetEmail=tk.Entry(font=("Arial",20))
            self.editGetEmail.grid(row=1,column=1)
            self.editGetEmail.insert(tk.INSERT,choice[1])
            self.editAskAddress=tk.Label(text="Address:",font=("Arial",20),width=50,height=50)
            self.editAskAddress.grid(row=2,column=0)
            self.editGetAddress=tk.Entry(font=("Arial",20))
            self.editGetAddress.grid(row=2,column=1)
            self.editGetAddress.insert(tk.INSERT,choice[2])
            self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=50, command=lambda: self.customersEditEntry())
            self.back.grid(row=6,column=0)           
            self.confirm=tk.Button(text="Confirm",font=("Arial",20),width=50,height=50, command=lambda: self.customersEditSave())
            self.confirm.grid(row=6,column=1)  

    def customersEditSave(self):
        self.customers[self.opt]=[self.editGetName.get(), self.editGetEmail.get(), self.editGetAddress.get()]  # Edit new information into the customer row
        self.customersConfirm()  # Save and reset dataframe and customer list
        time.sleep(1)  # Freeze page to show user information is being saved
        
    def customersView(self):
        self.customersNewScreen()
        self.customersDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.customersDisplay.grid(columnspan=5,row=0)
        self.customersDisplay.insert(tk.INSERT,self.customers_df.to_string(justify="right",col_space=25))
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.customersHome())
        self.back.grid(row=1,columnspan=5)  

    def customersDelete(self):
        self.customersNewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.customersHome())
        self.back.grid(column=0,row=1)   
        self.deleteDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name','Email','Address'],justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Customer Row Number",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.customersDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)
    
    def customersDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())  # Customer row to delete 
        if deleteRow>=len(self.customers) or deleteRow<0:  # If customer row provided is out of bounds
            self.customersDelete()  # Reset page
        else:
            self.customers.pop(deleteRow)  # Delete row
            self.customersConfirm()  # Save and update dataframe and customer row
            self.customersDelete()  # Reset page to also reset the textbox of customers
        time.sleep(1)  # Freeze page to show user information is being saved 
    
    def customersConfirm(self):
        with open(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Customers.csv", 'w') as csvfile:  # File as written mode
            csvwriter = csv.writer(csvfile)  # Create csv writing function
            self.customers.insert(0,['Name','Email','Address'])  # Putting titles back in to rewrite csv file correctly
            rows=0
            while rows < len(self.customers):
                csvwriter.writerow(self.customers[rows])  # Rewrite 2d array back into file
                rows += 1
        self.customers_df = pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Customers.csv", header=0)  # Updating dataframe
        self.customers.pop(0)  # Taking out titles from array to be back to original array of just customers
    
    def customersNewScreen(self):
        for widgets in window.winfo_children():
            widgets.destroy()



class Purchasing():
    def __init__(self):
        self.products_df = pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Products.csv", header=0)  # Make Dataframe
        self.products = self.products_df[['Name','SKU','Price A','Price B','Price C','Price D']].values  # Dataframe to numpy 2d array (w/o titles)
        self.products = self.products.tolist()  # Numpy array to regualar array (Only going to be used for editing)
        super().__init__()
    
    def purchasingHome(self):
        self.purchasingNewScreen()
        self.buttonAdd=tk.Button(text="Add to Purchasing",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingAdd())
        self.buttonAdd.grid(column=0,row=0)
        self.buttonDelete=tk.Button(text="Delete from Purchasing",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingDelete())
        self.buttonDelete.grid(column=0,row=1)
        self.buttonPayment=tk.Button(text="Payment",font=("Arial",25),width=100,height=200,command=lambda: self.payment())
        self.buttonPayment.grid(column=1,row=1)
        self.buttonView=tk.Button(text="View Purchasing",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingView())
        self.buttonView.grid(column=1,row=0)
        self.buttonBack=tk.Button(text="Home",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingBack())
        self.buttonBack.grid(columnspan=2)

    def purchasingAdd(self):  # Adding product to purchasing list
        self.purchasingNewScreen()
        self.purchasingDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.purchasingDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingHome())
        self.back.grid(column=0,row=1)   
        self.purchasingDisplay.insert(tk.INSERT,self.products_df.to_string(justify="right",col_space=25))
        self.purchasingChoose=tk.Label(text="Enter Product Row Number to Add to Purchasing List",font=("Arial",20),width=50,height=1)
        self.purchasingChoose.grid(column=1,row=0)
        self.purchasingEnter=tk.Entry(font=("Arial",20))
        self.purchasingEnter.grid(column=1,row=0,rowspan=2)
        self.purchasingButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingAddSave())
        self.purchasingButton.grid(column=1,row=1,rowspan=2)

    def purchasingAddSave(self):
        purchasing.append([len(purchasing),self.products[int(self.purchasingEnter.get())][0],self.products[int(self.purchasingEnter.get())][2]])  # Add purchasing item number, name, and price A
        time.sleep(1)  # Freeze page to show user information is being save                                                                                         
        
    def purchasingDelete(self):  # Deleting item in purchasing list
        self.purchasingNewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingHome())
        self.back.grid(column=0,row=1)   
        self.deleteDisplay.insert(tk.INSERT,purchasing)
        self.deleteChoose=tk.Label(text="Enter Purchasing List Row Number",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)  
            
    def purchasingDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())  # Row to delete
        if deleteRow>=len(purchasing) or deleteRow<0:  # If row is out of bounds
            self.purchasingDelete()  # Reset page
        else:
            purchasing.pop(deleteRow)  # Delete row
            self.purchasingDelete()  # Reset page to also reset text box
        time.sleep(1)  # Pause page to show user information is being saved
            
    def purchasingView(self):  # Viewing purchasing list
        self.purchasingNewScreen()
        self.purchasingDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.purchasingDisplay.grid(columnspan=5,row=0)
        self.purchasingDisplay.insert(tk.INSERT,purchasing)
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.purchasingHome())
        self.back.grid(row=1,columnspan=5)      
                
    def payment(self):   # Final payment and save to customer's purchases, and add to daily purchases file
        if len(purchasing)==0:
            print("Nothing in purchasing list")
            self.purchasingHome()  # Reload page
        a=0
        while a<len(purchasing):
            total=0
            total+=float(purchasing[a][1])  # Adding each price of item
            a+=1
        print("Total: $"+"{:.2f}".format(total))  # Print total
        self.purchasingHome()  # Reload page               
    
    def purchasingBack(self):
        self.purchasingNewScreen()
        run=GUI()

    def purchasingNewScreen(self):
        for widgets in window.winfo_children():
            widgets.destroy()        



class Invoices():
    def __init__(self):
        self.invoices_df=pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\SavedInvoices.csv", header=0)  # Dataframe
        self.invoices=self.invoices_df[['Invoice Number','Customer','Payed','Purchasing List']].values  # Dataframe to numpy array (w/o titles)
        self.invoices=self.invoices.tolist()  # Numpy array to regular list
        self.invoiceNum=0  # For determining new invoice number
        self.customers_df=pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\Customers.csv", header=0)
        self.customers=self.customers_df[['Name', 'Email','Address']].values  # Dataframe to numpy array (w/o titles)
        self.customers=self.customers.tolist()  # Numpy array to regular list
        self.invoicesRowNum=0  # Row number for customer/invoice list
        self.Payed=""  # String for determining if invoice is payed or not
        super().__init__()

    def invoicesHome(self):
        self.invoicesNewScreen()
        self.buttonAdd=tk.Button(text="Save Invoice to Customer",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesEntry())
        self.buttonAdd.grid(row=0,column=0)
        self.buttonEdit=tk.Button(text="View Invoices",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesView())
        self.buttonEdit.grid(row=0,column=1)
        self.buttonDelete=tk.Button(text="Edit Invoices",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesEditEntry())
        self.buttonDelete.grid(row=1,column=0)
        self.buttonView=tk.Button(text="Delete Invoice",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesDelete())
        self.buttonView.grid(row=1,column=1)
        self.buttonBack=tk.Button(text="Home",font=("Arial",25),width=100,height=200,command=lambda: self.Return())
        self.buttonBack.grid(columnspan=2)
        
    def invoicesEntry(self):    
        self.invoicesNewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesHome())
        self.back.grid(column=0,row=1,rowspan=2)   
        self.invoicesDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name'],justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="Enter Customer Row Number to Add Invoice to",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesRow=tk.Entry(font=("Arial",20))
        self.invoicesRow.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesSave())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)
        
    def invoicesSave(self):
        self.invoicesRowNum=int(self.invoicesRow.get())
        if self.invoicesRowNum>=len(self.customers) or self.invoicesRowNum<0:
            self.invoicesEntry()
        else:
            self.invoicesNewScreen()
            self.invoicesDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
            self.invoicesDisplay.grid(column=0,row=0)
            self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesEntry())
            self.back.grid(column=0,row=1)   
            self.invoicesDisplay.insert(tk.INSERT,purchasing)
            self.invoicesPayed=tk.Label(text="Invoice Payed? Press Button Then Press Confirm",font=("Arial",20),width=50,height=1)
            self.invoicesPayed.grid(column=1,row=0,columnspan=4)
            self.invoicesYesButton=tk.Button(text="Yes",font=("Arial",20),width=3,height=2,command=lambda: self.invoicesYes())
            self.invoicesYesButton.grid(column=1,row=0,rowspan=2)
            self.invoicesNoButton=tk.Button(text="No",font=("Arial",20),width=3,height=2,command=lambda: self.invoicesNo())
            self.invoicesNoButton.grid(column=1,row=0,rowspan=2,columnspan=8)            
            self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesSave2())
            self.invoicesButton.grid(column=1,row=1,rowspan=2)            
        
    def invoicesYes(self):
        self.Payed="Yes"  # Invoice is paid
        time.sleep(1)  # Pause screen to show user input is being saved
    
    def invoicesNo(self):
        self.Payed="No"  # Invoice is not paid
        time.sleep(1)   # Pause screen to show user input is being saved
    
    def invoicesSave2(self):
        self.invoicesNumcheck()  # Get next invoice number
        self.invoices.append([self.invoiceNum,self.customers[self.invoicesRowNum][0],self.Payed,purchasing])  # Add onto invoices list if it is a new customer
        self.invoicesConfirm()  # Save and update dataframe and invoices list
        time.sleep(1)  # Pause screen to show user that information is being saved
        
    def invoicesNumcheck(self):                
        if len(self.invoices)==1:  # If invoices list has only one customer on it
                self.invoiceNum=int(self.invoices[0][0])+1  # If only one invoice number with the customer, the next invoice number is that plus 1
        else:
            a=1
            while a<len(self.invoices):  # If the list of invoices has more than one customer
                if self.invoiceNum<int(self.invoices[a][0]):  # If the current invoice number is less than the next invoice number of that certain customer
                    if int(self.invoices[a][0])>int(self.invoices[a-1][0]):  # If that invoice number is greater than the one of the previous customer
                        self.invoiceNum=self.invoices[a][0]+1  # New invoice number is that customer's plus 1
                    else:
                        self.invoiceNum=self.invoices[a-1][0]+1  # New invoice number is the previous customer's plus 1
                a+=1

    def invoicesEditEntry(self):
        self.invoicesNewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesHome())
        self.back.grid(column=0,row=1,rowspan=2)   
        self.invoicesDisplay.insert(tk.INSERT,self.invoices_df.to_string(columns=['Invoice Number','Customer','Payed','Purchasing List'],justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="Enter Invoice Row to Edit",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesRowEntry=tk.Entry(font=("Arial",20))
        self.invoicesRowEntry.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesEditChoice())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)

    def invoicesEditChoice(self):
        self.invoicesRowNum=int(self.invoicesRowEntry.get())
        if self.invoicesRowNum>=len(self.invoices) or self.invoicesRowNum<0:
            self.invoicesEditEntry()
        else:
            self.invoicesNewScreen()
            self.buttonCustomer=tk.Button(text="Edit Customer",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesCustomerEdit())
            self.buttonCustomer.grid(row=0,column=0)
            self.buttonPurchasing=tk.Button(text="Edit Purchasing List",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesPurchasingEdit())
            self.buttonPurchasing.grid(row=0,column=1)
            self.buttonPayedStatus=tk.Button(text="Edit Payed Status",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesPayedEdit())
            self.buttonPayedStatus.grid(row=1,column=0)
            self.buttonReturn=tk.Button(text="Back",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesEditEntry())
            self.buttonReturn.grid(row=1,column=1)
    
    def invoicesCustomerEdit(self):
        self.invoicesNewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesEditEntry())
        self.back.grid(column=0,row=1,rowspan=2)   
        self.invoicesDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name'],justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="Enter Customer Row Number to Change Invoice to",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesEditRow=tk.Entry(font=("Arial",20))
        self.invoicesEditRow.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesCustomerEditSave())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)

    def invoicesPurchasingEdit(self):
        self.invoicesNewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesEditEntry())
        self.back.grid(column=0,row=1,rowspan=2)   
        self.invoicesDisplay.insert(tk.INSERT,purchasing)
        self.invoicesChoose=tk.Label(text="<--New Purchasing List?\n",font=("Arial",20),width=55,height=2)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesPurchasingEditSave())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)    
    
    def invoicesPayedEdit(self):
        self.invoicesNewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesEditEntry())
        self.back.grid(column=0,row=1)   
        self.invoicesDisplay.insert(tk.INSERT,purchasing)
        self.invoicesPayed=tk.Label(text="Invoice is currently "+str(self.invoices[self.invoicesRowNum][2])+"\nChange to:",font=("Arial",20),width=50,height=2)
        self.invoicesPayed.grid(column=1,row=0,columnspan=4)
        self.invoicesYesButton=tk.Button(text="Yes",font=("Arial",20),width=3,height=2,command=lambda: self.invoicesYes())
        self.invoicesYesButton.grid(column=1,row=0,rowspan=2)
        self.invoicesNoButton=tk.Button(text="No",font=("Arial",20),width=3,height=2,command=lambda: self.invoicesNo())
        self.invoicesNoButton.grid(column=1,row=0,rowspan=2,columnspan=8)            
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesPayedEditSave())
        self.invoicesButton.grid(column=1,row=1,rowspan=2)    
    
    def invoicesCustomerEditSave(self):
        if self.invoicesRowNum>=len(self.customers) or self.invoicesRowNum<0:
            self.invoicesCustomerEdit()
        else:
            self.invoices[self.invoicesRowNum][1]=self.customers[int(self.invoicesEditRow.get())][0]
            self.invoicesConfirm()
        time.sleep(1)  # Pause screen to show user that information is being saved

    def invoicesPurchasingEditSave(self):
        self.invoices[self.invoicesRowNum][3]=purchasing
        self.invoicesConfirm()
        time.sleep(1)  # Pause screen to show user that information is being saved

    def invoicesPayedEditSave(self):
        self.invoices[self.invoicesRowNum][2]=self.Payed
        self.invoicesConfirm()
        time.sleep(1)  # Pause screen to show user that information is being saved

    def invoicesView(self):
        self.invoicesNewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(columnspan=5,row=0)
        self.invoicesDisplay.insert(tk.INSERT,self.invoices_df.to_string(justify="right",col_space=25))
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.invoicesHome())
        self.back.grid(row=1,columnspan=5)  

    def invoicesDelete(self):
        self.invoicesNewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesHome())
        self.back.grid(column=0,row=1)   
        self.deleteDisplay.insert(tk.INSERT,self.invoices_df.to_string(columns=['Customer','Payed','Purchasing List'],justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Invoice Row Number to Delete",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)
    
    def invoicesDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())  # Invoice row to delete 
        if deleteRow>=len(self.invoices) or deleteRow<0:  # If invoice row provided is out of bounds
            self.invoicesDelete()  # Reset page
        else:
            self.invoices.pop(deleteRow)  # Delete row
            self.invoicesConfirm()  # Save and update dataframe and invoice row
            self.invoicesDelete()  # Reset page to also reset the textbox of invoices
        time.sleep(1)  # Freeze page to show user information is being saved 

    def invoicesConfirm(self):
        with open(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\SavedInvoices.csv", 'w') as csvfile:  # File as written mode
            csvwriter = csv.writer(csvfile)  # Create csv writing function
            self.invoices.insert(0,['Invoice Number','Customer','Payed','Purchasing List'])  # Putting titles back in to rewrite csv file correctly
            rows=0
            while rows < len(self.invoices):
                csvwriter.writerow(self.invoices[rows])  # Rewrite 2d array back into file
                rows += 1
        self.invoices_df = pd.read_csv(r"C:\Users\Adriel\OneDrive\Documents\GitHub\Python-Projects\BusinessApp\SavedInvoices.csv", header=0)  # Updating dataframe
        self.invoices.pop(0)  # Taking out titles from array to be back to original array of invoices

    def invoicesNewScreen(self):
        for widgets in window.winfo_children():
            widgets.destroy()         

        

class GUI(Products, Customers, Purchasing, Invoices):
    def __init__(self):
        super().__init__()             
        self.buttonProducts=tk.Button(text="Products",font=("Arial",25),width=1280,height=720, command=lambda: self.productsHome())
        self.buttonProducts.grid(row=0,column=0)
        self.buttonCustomers=tk.Button(text="Customers",font=("Arial",25),width=1280,height=720, command=lambda: self.customersHome())
        self.buttonCustomers.grid(row=0,column=1)
        self.buttonPurchasing=tk.Button(text="Purchasing",font=("Arial",25),width=1280,height=720, command=lambda: self.purchasingHome())
        self.buttonPurchasing.grid(row=1,column=0)
        self.buttonInvoices=tk.Button(text="Invoices",font=("Arial",25),width=1280,height=720, command=lambda: self.invoicesHome())
        self.buttonInvoices.grid(row=1,column=1)   



window=tk.Tk()   
window.title("Business App")
window.geometry("2560x1440")
run=GUI()
window.columnconfigure([0,1,2,3,4,5,6],weight=1)
window.rowconfigure([0,1,2,3,4,5,6],weight=1)
window.mainloop()     

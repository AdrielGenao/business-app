from tkinter.constants import INSERT
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
import time
import mysql.connector

# Setup for MySQL connection and editing
mydb = mysql.connector.connect(
                    host="sql5.freemysqlhosting.net",
                    user="sql5435762",
                    password="AQDpUyXDyU",
                    database="sql5435762")
cursor = mydb.cursor()



class Products():  # Products class for creating, editing, viewing, and deleting products
    def __init__(self):
        self.products_df = pd.read_sql_query('SELECT * FROM sql5435762.Products',mydb)  # Make Dataframe from SQL Database
        self.products_df.index+=1
        self.products = self.products_df[['Name','SKU','Price A','Price B','Price C','Price D']].values  # Dataframe to numpy 2d array
        self.products = self.products.tolist()  # Numpy array to regular array (Only going to be used for editing)
        super().__init__()            
    
    def productsHome(self):
        self.NewScreen()
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
        self.NewScreen()
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
        cursor.execute("""
                INSERT INTO sql5435762.Products(Name,SKU,`Price A`,`Price B`,`Price C`,`Price D`)
                VALUES
                ('"""+newRow[0].replace("'", "\\'")+"""','"""+newRow[1]+"""','"""+newRow[2]+"""','"""+newRow[3]+"""','"""+newRow[4]+"""','"""+newRow[5]+"""')
                """)
        mydb.commit()
        self.products_df = pd.read_sql_query('SELECT * FROM sql5435762.Products',mydb)  # Make Dataframe
        self.products_df.index+=1
        self.products=sorted(self.products,key=lambda x: x[0])  # Sorting Products list to match alphabetically sorting of DataFrame
        time.sleep(1)  # Pause to show user that product is being saved to file      

    def productsEditChoice(self):
        self.NewScreen()
        self.productsDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))  # Text box for products display
        self.productsDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.productsHome())
        self.back.grid(column=0,row=1)
        if len(self.products)==0:  # If nothing in products list (No products added or in database)
            self.productsDisplay.insert(tk.INSERT,"No Products")
        else:
            self.productsDisplay.insert(tk.INSERT,self.products_df.to_string(columns=['Name','SKU'],justify="right",col_space=25))  # Printing names and SKU's of products
        self.productChoose=tk.Label(text="Enter Product Row Number",font=("Arial",20),width=50,height=1)
        self.productChoose.grid(column=1,row=0)
        self.productEnter=tk.Entry(font=("Arial",20))
        self.productEnter.grid(column=1,row=0,rowspan=2)
        self.productButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.productsEdit())
        self.productButton.grid(column=1,row=1,rowspan=2)

    def productsEdit(self):    
        self.opt=int(self.productEnter.get())-1  # Row of product to edit
        self.NewScreen()
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
        previous=self.products[self.opt]  # Previous variable to use for MySQL query to change product
        self.products[self.opt]=[self.editGetName.get(), self.editGetSKU.get(), self.editGetPriceA.get(), self.editGetPriceB.get(), self.editGetPriceC.get(), self.editGetPriceD.get()]  # Row of newly edited product
        cursor.execute("""
                UPDATE sql5435762.Products
                SET Name='"""+self.editGetName.get().replace("'", "\\'")+"""',SKU='"""+self.editGetSKU.get()+"""',`Price A`='"""+self.editGetPriceA.get()+"""',`Price B`='"""+self.editGetPriceB.get()+"""',`Price C`='"""+self.editGetPriceC.get()+"""',`Price D`='"""+self.editGetPriceD.get()+"""'
                WHERE Name ='"""+previous[0].replace("'", "\\'")+"""'""")
        mydb.commit()        
        self.products_df = pd.read_sql_query('SELECT * FROM sql5435762.Products',mydb)  # Reset Dataframe to new values
        self.products_df.index+=1
        self.products=sorted(self.products,key=lambda x: x[0])  # Sorting Products list to match alphabetically sorting of DataFrame
        time.sleep(1)  # Pause screen to show user that the product is being saved
        self.productsEditChoice()

    def productsView(self):
        self.NewScreen()
        self.productsDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.productsDisplay.grid(columnspan=5,row=0)
        if len(self.products)==0:  # If nothing in products list (No products added or in database)
            self.productsDisplay.insert(tk.INSERT,"No Products")
        else:
            self.productsDisplay.insert(tk.INSERT,self.products_df.to_string(index=False,justify="right",col_space=25))
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.productsHome())
        self.back.grid(row=1,columnspan=5)  
        
    def productsDelete(self):
        self.NewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.productsHome())
        self.back.grid(column=0,row=1)   
        if len(self.products)==0:  # If nothing in products list(No products added or in database)
            self.deleteDisplay.insert(tk.INSERT,"No Products")
        else:
            self.deleteDisplay.insert(tk.INSERT,self.products_df.to_string(columns=['Name','SKU'],justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Product Row Number",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.productsDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)
    
    def productsDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())-1  # Row of product to delete
        deleteRowName = self.products[deleteRow][0]  # Name of product in delete row for reference for MySQL
        if deleteRow>=len(self.products) or deleteRow<0:  # If entry was out of bounds of product list
            self.productsDelete()  # Reset page
        else:
            self.products.pop(deleteRow)  # Delete row from list of products
            cursor.execute("""
                DELETE FROM sql5435762.Products
                WHERE Name ='"""+str(deleteRowName)+"""'""")
            mydb.commit()        
            self.products_df = pd.read_sql_query('SELECT * FROM sql5435762.Products',mydb)  # Reset Dataframe to new values
            self.products_df.index+=1
            self.products=sorted(self.products,key=lambda x: x[0])  # Sorting Products list to match alphabetically sorting of DataFrame
            time.sleep(1)  # Pause page to show user that product is being deleted  
            self.productsDelete()   # Refresh page to reset textbox of products    

    def NewScreen(self):  # Function that clears page to create a new one when changing pages
        for widgets in window.winfo_children():
            widgets.destroy()  # Delete all widgets on page to create new one

    def Return(self):  # Function for returning to home screen by resetting GUI
        self.NewScreen()
        run=GUI()



class Customers:  # Customer class for creating, editing, viewing, and deleting customers
    def __init__(self):
        self.customers_df=pd.read_sql_query('SELECT * FROM sql5435762.Customers',mydb)  # Dataframe
        self.customers_df.index+=1
        self.customers=self.customers_df[['Name','Email','Address']].values  # Dataframe to numpy array (w/o titles)
        self.customers=self.customers.tolist()  # Numpy array to regular list
        super().__init__()    
        
    def customersHome(self):
        self.NewScreen()
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
        self.NewScreen()
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
        cursor.execute("""
                INSERT INTO sql5435762.Customers(Name,Email,Address)
                VALUES
                ('"""+self.CustomersAddGetName.get().replace("'", "\\'")+"""','"""+self.addGetEmail.get().replace("'", "\\'")+"""','"""+self.addGetAddress.get().replace("'", "\\'")+"""')
                """)
        mydb.commit()        
        self.customers_df = pd.read_sql_query('SELECT * FROM sql5435762.Customers',mydb)  # Make Dataframe
        self.customers_df.index+=1
        self.customers=sorted(self.customers,key=lambda x: x[0])  # Sorting Customers list to match alphabetically sorting of DataFrame 
        time.sleep(1)  # Freeze page to show user that product is being added
          
    def customersEditEntry(self):
        self.NewScreen()
        self.customersDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.customersDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.customersHome())
        self.back.grid(column=0,row=1)   
        if len(self.customers)==0:  # If nothing in customers list(No customers added or in database)
            self.customersDisplay.insert(tk.INSERT,"No Customers")
        else:
            self.customersDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name','Email','Address'],justify="right",col_space=25))
        self.customerChoose=tk.Label(text="Enter Customer Row Number",font=("Arial",20),width=50,height=1)
        self.customerChoose.grid(column=1,row=0)
        self.customerEnter=tk.Entry(font=("Arial",20))
        self.customerEnter.grid(column=1,row=0,rowspan=2)
        self.customerButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.customersEdit())
        self.customerButton.grid(column=1,row=1,rowspan=2)   

    def customersEdit(self):
        self.opt=int(self.customerEnter.get())-1  # Get customer row number
        self.NewScreen()  # Clear page
        if self.opt>=len(self.customers) or self.opt<0: # If customer row number input is out of bounds 
            self.customersEditEntry()  # Reset page
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
        previous = self.customers[self.opt]
        self.customers[self.opt]=[self.editGetName.get(), self.editGetEmail.get(), self.editGetAddress.get()]  # Edit new information into the customer row
        cursor.execute("""
                UPDATE sql5435762.Customers
                SET Name='"""+self.editGetName.get().replace("'", "\\'")+"""',Email='"""+self.editGetEmail.get().replace("'", "\\'")+"""',Address='"""+self.editGetAddress.get().replace("'", "\\'")+"""'
                WHERE Name ='"""+previous[0].replace("'", "\\'")+"""'""")
        mydb.commit()        
        self.customers_df = pd.read_sql_query('SELECT * FROM sql5435762.Customers',mydb)  # Reset Dataframe to new values
        self.customers_df.index+=1
        self.customers=sorted(self.customers,key=lambda x: x[0])  # Sorting Customers list to match alphabetically sorting of DataFrame        
        time.sleep(1)  # Freeze page to show user information is being saved
        self.customersEditEntry()
        
    def customersView(self):
        self.NewScreen()
        self.customersDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.customersDisplay.grid(columnspan=5,row=0)
        if len(self.customers)==0:  # If nothing in customers list(No customers added or in database)
            self.customersDisplay.insert(tk.INSERT,"No Customers")
        else:
            self.customersDisplay.insert(tk.INSERT,self.customers_df.to_string(justify="right",col_space=25))
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.customersHome())
        self.back.grid(row=1,columnspan=5)  

    def customersDelete(self):
        self.NewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.customersHome())
        self.back.grid(column=0,row=1)   
        if len(self.customers)==0:  # If nothing in customers list(No customers added or in database)
            self.deleteDisplay.insert(tk.INSERT,"No Customers")
        else:
            self.deleteDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name','Email','Address'],justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Customer Row Number",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.customersDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)
    
    def customersDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())-1  # Customer row to delete
        deleteRowName=self.customers[deleteRow][0]
        if deleteRow>=len(self.customers) or deleteRow<0:  # If customer row provided is out of bounds
            self.customersDelete()  # Reset page
        else:
            self.customers.pop(deleteRow)  # Delete row
            cursor.execute("""
                DELETE FROM sql5435762.Customers
                WHERE Name ='"""+deleteRowName.replace("'", "\\'")+"""'""")
            mydb.commit()        
            self.customers_df = pd.read_sql_query('SELECT * FROM sql5435762.Customers',mydb)  # Reset Dataframe to new values
            self.customers_df.index+=1    
            self.customers=sorted(self.customers,key=lambda x: x[0])  # Sorting Customers list to match alphabetically sorting of DataFrame 
            time.sleep(1)  # Freeze page to show user information is being saved 
            self.customersDelete()  # Reset page to also reset the textbox of customers



purchasing=[]

class Purchasing():  # Purchasing class for payments and creating a purchasing list of products
    def __init__(self):
        super().__init__()
        self.purchasingDF=pd.DataFrame(purchasing,columns=['Name','Quantity','Price'])
        self.purchasingDF.index+=1
    
    def purchasingHome(self):
        self.NewScreen()
        self.buttonAdd=tk.Button(text="Add to Purchasing",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingAddName())
        self.buttonAdd.grid(column=0,row=0)
        self.buttonDelete=tk.Button(text="Delete from Purchasing",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingDelete())
        self.buttonDelete.grid(column=0,row=1)
        self.buttonPayment=tk.Button(text="Retrieve Purchasing List from Saved Invoice",font=("Arial",25),width=100,height=200,command=lambda: self.InvoicetoPurchasingEntry())
        self.buttonPayment.grid(column=1,row=1)
        self.buttonView=tk.Button(text="View Purchasing + Total Amount",font=("Arial",25),width=100,height=200,command=lambda: self.purchasingView())
        self.buttonView.grid(column=1,row=0)
        self.buttonBack=tk.Button(text="Home",font=("Arial",25),width=100,height=200,command=lambda: self.Return())
        self.buttonBack.grid(columnspan=2)

    def purchasingAddName(self):  # Adding product to purchasing list
        self.NewScreen()
        self.purchasingDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.purchasingDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingHome())
        self.back.grid(column=0,row=1)   
        self.purchasingDisplay.insert(tk.INSERT,self.products_df.to_string(justify="right",col_space=25))
        self.purchasingChoose=tk.Label(text="Enter Product Row Number to Add to Purchasing List",font=("Arial",20),width=50,height=1)
        self.purchasingChoose.grid(column=1,row=0)
        self.purchasingEnter=tk.Entry(font=("Arial",20))
        self.purchasingEnter.grid(column=1,row=0,rowspan=2)
        self.purchasingButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingAddNameSave())
        self.purchasingButton.grid(column=1,row=1,rowspan=2)

    def purchasingAddNameSave(self):
        if int(self.purchasingEnter.get())-1>=len(self.products) or int(self.purchasingEnter.get())-1<0:
            self.purchasingAddName()
        else:
            self.purchasingName=self.products[int(self.purchasingEnter.get())-1][0]
            self.purchasingPrice=self.products[int(self.purchasingEnter.get())-1][2]
            self.purchasingAddDF=pd.DataFrame([[self.purchasingName,self.purchasingPrice]],columns=['Name','Price'])
            self.NewScreen()
            self.purchasingDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
            self.purchasingDisplay.grid(column=0,row=0)
            self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingAddName())
            self.back.grid(column=0,row=1)   
            self.purchasingDisplay.insert(tk.INSERT,self.purchasingAddDF.to_string(index=False,justify="right",col_space=25))
            self.purchasingChoose=tk.Label(text="How Many/Quantity of the Product for the Purchasing List?",font=("Arial",20),width=50,height=1)
            self.purchasingChoose.grid(column=1,row=0)
            self.purchasingEnter=tk.Entry(font=("Arial",20))
            self.purchasingEnter.grid(column=1,row=0,rowspan=2)
            self.purchasingButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingAddQuantitySave())
            self.purchasingButton.grid(column=1,row=1,rowspan=2)
                                                                                                     
    def purchasingAddQuantitySave(self):
        if self.purchasingEnter.get().isnumeric():
            self.newPurchasingRow=[[self.purchasingName,self.purchasingEnter.get(),self.purchasingPrice]]
        else:
            self.newPurchasingRow=[[self.purchasingName,'0',self.purchasingPrice]]
        purchasing.append(self.newPurchasingRow[0])
        self.purchasingDF=pd.DataFrame(purchasing,columns=['Product Name','Quantity','Price'])
        self.purchasingDF.index+=1
        time.sleep(1)  # Freeze page to show user information is being save
        self.purchasingAddName()  # Return back to choosing name of product to add to purchasing list screen
    
    def purchasingDelete(self):  # Deleting item in purchasing list
        self.NewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingHome())
        self.back.grid(column=0,row=1)   
        if len(purchasing)==0:  # If nothing was added to purchasing list
            self.deleteDisplay.insert(tk.INSERT,"Nothing in Purchasing List")
        else:
            self.deleteDisplay.insert(tk.INSERT,self.purchasingDF.to_string(justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Purchasing List Row Number",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.purchasingDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)  
            
    def purchasingDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())-1  # Row to delete
        if deleteRow>=len(purchasing) or deleteRow<0:  # If row is out of bounds
            self.purchasingDelete()  # Reset page
        else:
            purchasing.pop(deleteRow)  # Delete row
            self.purchasingDF = pd.DataFrame(purchasing,columns=['Product Name','Quantity','Price'])
            self.purchasingDF.index+=1
            self.purchasingDelete()  # Reset page to also reset text box
        time.sleep(1)  # Pause page to show user information is being saved
            
    def InvoicetoPurchasingEntry(self):  
        self.NewScreen()
        self.purchasingDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.purchasingDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.purchasingHome())
        self.back.grid(column=0,row=1,rowspan=2)
        if len(self.invoices)==0:  # If nothing in invoices list(No invoices added or in database)
            self.purchasingDisplay.insert(tk.INSERT,"No Invoices Saved")
        else: 
            self.purchasingDisplay.insert(tk.INSERT,self.invoices_df.to_string(index=False,columns=['Invoice Number','Customer','Payed','Purchasing List'],justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="Enter Invoice Number to take Purchasing List of",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.purchasingRowEntry=tk.Entry(font=("Arial",20))
        self.purchasingRowEntry.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.purchasingInvoiceChoice())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)

    def purchasingInvoiceChoice(self):
        self.invoicesNumber=int(self.purchasingRowEntry.get())  # Get invoice number chosen
        if self.invoicesNumber>self.invoiceNum or self.invoicesNumber<=0:
            self.InvoicetoPurchasingEntry() # Reset choosing screen
        else:
            for i in range(len(self.invoices)):  # Changing self.invoicesRowNum from the invoice number the user provided to the actual row number to use for the invoices list
                if self.invoices[i][0]==self.invoicesNumber:
                    self.invoicesRowNum=i  # invoicesRowNum will be used for list editing and saving
            self.NewScreen()
            self.purchasingDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
            self.purchasingDisplay.grid(column=0,row=0)
            self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.InvoicetoPurchasingEntry())
            self.back.grid(column=0,row=1,rowspan=2)
            self.invoicesPurchasing=self.invoices[self.invoicesRowNum][3]
            self.invoicesPurchasing=(self.invoicesPurchasing[2:len(self.invoicesPurchasing)-2].replace("'","")).split(", ")
            self.purchasingDFDemo=pd.DataFrame([self.invoicesPurchasing],columns=['Product Name','Quantity','Price'])
            self.purchasingDisplay.insert(tk.INSERT,self.purchasingDFDemo.to_string(index=False,justify="right",col_space=25))
            self.invoicesChoose=tk.Label(text="<-- New Purchasing List?\n",font=("Arial",20),width=55,height=2)
            self.invoicesChoose.grid(column=1,row=0,rowspan=2)
            self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.PurchasingInvoiceConfirm())
            self.invoicesButton.grid(column=1,row=2,rowspan=2) 

    def PurchasingInvoiceConfirm(self):
        purchasing.clear()
        purchasing.append(self.invoicesPurchasing)
        self.purchasingDF = pd.DataFrame(purchasing,columns=['Product Name','Quantity','Price'])
        self.purchasingDF.index+=1
    
    def purchasingView(self):  # Viewing purchasing list + Total Amount
        self.NewScreen()
        self.purchasingDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.purchasingDisplay.grid(columnspan=5,row=0)
        subtotal=0
        if(len(self.purchasingDF)==0):  # If nothing was added to purchasing list
            self.purchasingDisplay.insert(tk.INSERT,"Nothing in Purchasing List")
        else:  # If purchasing list does cotain products added
            purchasing = self.purchasingDF[['Product Name','Quantity','Price']].values  # Dataframe to numpy 2d array
            purchasing = purchasing.tolist()  # Numpy array to regular array (Only going to be used for editing)
            for i in range(len(purchasing)):
                subtotal+=float(float(purchasing[i][2])*int(purchasing[i][1]))
            self.purchasingDisplay.insert(tk.INSERT,self.purchasingDF.to_string(justify="right",col_space=25)+"\nSubtotal: $"+"{:.2f}".format(subtotal)+"\nSales Tax: 6.00%\nTotal: $"+"{:.2f}".format(subtotal+subtotal*.06)) 
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.purchasingHome())
        self.back.grid(row=1,columnspan=5)  

class Invoices():  # Invoices class for saving, editing, viewing, and deleting saved invoices
    def __init__(self):
        self.invoices_df=pd.read_sql_query('SELECT * FROM sql5435762.SavedInvoices',mydb)  # Dataframe
        self.invoices=self.invoices_df[['Invoice Number','Customer','Payed','Purchasing List']].values  # Dataframe to numpy array
        self.invoiceNum_df=pd.read_sql_query('SELECT * FROM sql5435762.NextInvoiceNumber',mydb)  # Dataframe for determining next invoice number
        self.invoiceNumList=self.invoiceNum_df['Next'].values  # Numpy array of dataframe
        self.invoiceNum=self.invoiceNumList[0]  # Variable to be used to determine the next invoice number to be assigned
        self.invoices=self.invoices.tolist()  # Numpy array to regular list
        self.invoicesRowNum=0  # Row number for customer/invoice list
        self.Payed=""  # String for determining if invoice is payed or not
        super().__init__()

    def invoicesHome(self):
        self.NewScreen()
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
        self.NewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesHome())
        self.back.grid(column=0,row=1,rowspan=2)   
        if len(self.customers)==0:  # If nothing in customers list(No customers added or in database)
            self.invoicesDisplay.insert(tk.INSERT,"No Customers")
        else:
            self.invoicesDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name'],justify="right",col_space=25))   
        self.invoicesChoose=tk.Label(text="Enter Customer Row Number to Add Invoice to",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesRow=tk.Entry(font=("Arial",20))
        self.invoicesRow.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesSave())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)
        
    def invoicesSave(self):
        self.invoicesRowNum=int(self.invoicesRow.get())-1
        if self.invoicesRowNum>=len(self.customers) or self.invoicesRowNum<0:
            self.invoicesEntry()
        else:
            self.NewScreen()
            self.invoicesDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
            self.invoicesDisplay.grid(column=0,row=0)
            self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesEntry())
            self.back.grid(column=0,row=1)   
            if len(purchasing)==0:  # If nothing in purchasing list
                self.invoicesDisplay.insert(tk.INSERT,"Nothing in Purchasing List")
            else:
                self.invoicesDisplay.insert(tk.INSERT,self.purchasingDF.to_string(justify="right",col_space=25))
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
        self.invoices.append([self.invoiceNum,self.customers[self.invoicesRowNum][0],self.Payed,purchasing])  # Add new saved invoice onto invoices list
        cursor.execute("""
                INSERT INTO sql5435762.SavedInvoices(`Invoice Number`,Customer,Payed,`Purchasing List`)
                VALUES
                ("""+str(self.invoiceNum)+""",'"""+self.customers[self.invoicesRowNum][0].replace("'", "\\'")+"""','"""+self.Payed+"""','"""+str(purchasing).replace("'", "\\'")+"""')
                """)
        mydb.commit() # Save to MySQL database
        self.invoices_df = pd.read_sql_query('SELECT * FROM sql5435762.SavedInvoices',mydb)  # Reset Dataframe to new values
        time.sleep(1)  # Pause screen to show user that information is being saved
        
    def invoicesNumcheck(self):  # Method for getting newest invoice number based on MySQL Table holding the current highest invoice number     
        cursor.execute(""" 
                UPDATE sql5435762.NextInvoiceNumber
                SET Next = Next+1
                Where Next = """+str(self.invoiceNum)+"""
                """)
        mydb.commit()
        self.invoiceNum+=1

    def invoicesEditEntry(self):
        self.NewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesHome())
        self.back.grid(column=0,row=1,rowspan=2)
        if len(self.invoices)==0:  # If nothing in invoices list(No invoices added or in database)
            self.invoicesDisplay.insert(tk.INSERT,"No Invoices Saved")
        else: 
            self.invoicesDisplay.insert(tk.INSERT,self.invoices_df.to_string(index=False,columns=['Invoice Number','Customer','Payed','Purchasing List'],justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="Enter Invoice Number to Edit",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesRowEntry=tk.Entry(font=("Arial",20))
        self.invoicesRowEntry.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesEditChoice())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)

    def invoicesEditChoice(self):
        self.invoicesNumber=int(self.invoicesRowEntry.get())  # InvoicesNumber will be used for MySQL editing and saving
        if self.invoicesNumber>self.invoiceNum or self.invoicesNumber<=0:
            self.invoicesEditEntry()
        else:
            for i in range(len(self.invoices)):  # Changing self.invoicesRowNum from the invoice number the user provided to the actual row number to use for the invoices list
                if self.invoices[i][0]==self.invoicesNumber:
                    self.invoicesRowNum=i  # invoicesRowNum will be used for list editing and saving
            self.NewScreen()
            self.buttonCustomer=tk.Button(text="Edit Customer",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesCustomerEdit())
            self.buttonCustomer.grid(row=0,column=0)
            self.buttonPurchasing=tk.Button(text="Edit Purchasing List",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesPurchasingEdit())
            self.buttonPurchasing.grid(row=0,column=1)
            self.buttonPayedStatus=tk.Button(text="Edit Payed Status",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesPayedEdit())
            self.buttonPayedStatus.grid(row=1,column=0)
            self.buttonReturn=tk.Button(text="Back",font=("Arial",25),width=100,height=200,command=lambda: self.invoicesEditEntry())
            self.buttonReturn.grid(row=1,column=1)
    
    def invoicesCustomerEdit(self):
        self.NewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesEditEntry())
        self.back.grid(column=0,row=1,rowspan=2)   
        if len(self.customers)==0:  # If nothing in customers list(No customers added or in database)
            self.invoicesDisplay.insert(tk.INSERT,"No Customers")
        else: 
            self.invoicesDisplay.insert(tk.INSERT,self.customers_df.to_string(columns=['Name'],justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="Enter Customer Row Number to Change Invoice to",font=("Arial",20),width=55,height=1)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesEditRow=tk.Entry(font=("Arial",20))
        self.invoicesEditRow.grid(column=1,row=0,rowspan=4)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesCustomerEditSave())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)

    def invoicesPurchasingEdit(self):
        self.NewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=120,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesEditEntry())
        self.back.grid(column=0,row=1,rowspan=2)
        if len(purchasing)==0:  # If nothing in purchasing list
            self.invoicesDisplay.insert(tk.INSERT,"Nothing in Purchasing List")
        else: 
            self.invoicesDisplay.insert(tk.INSERT,self.purchasingDF.to_string(justify="right",col_space=25))
        self.invoicesChoose=tk.Label(text="<--New Purchasing List?\n",font=("Arial",20),width=55,height=2)
        self.invoicesChoose.grid(column=1,row=0,rowspan=2)
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=40,height=6, command=lambda: self.invoicesPurchasingEditSave())
        self.invoicesButton.grid(column=1,row=2,rowspan=2)    
    
    def invoicesPayedEdit(self):
        self.NewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesEditEntry())
        self.back.grid(column=0,row=1)
        if len(purchasing)==0:  # If nothing in purchasing list
            self.invoicesDisplay.insert(tk.INSERT,"Nothing in Purchasing List")
        else: 
            self.invoicesDisplay.insert(tk.INSERT,self.purchasingDF.to_string(justify="right",col_space=25))  
        self.invoicesPayed=tk.Label(text="Invoice is currently "+str(self.invoices[self.invoicesRowNum][2])+"\nChange to:",font=("Arial",20),width=50,height=2)
        self.invoicesPayed.grid(column=1,row=0,columnspan=4)
        self.invoicesYesButton=tk.Button(text="Yes",font=("Arial",20),width=3,height=2,command=lambda: self.invoicesYes())
        self.invoicesYesButton.grid(column=1,row=0,rowspan=2)
        self.invoicesNoButton=tk.Button(text="No",font=("Arial",20),width=3,height=2,command=lambda: self.invoicesNo())
        self.invoicesNoButton.grid(column=1,row=0,rowspan=2,columnspan=8)            
        self.invoicesButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesPayedEditSave())
        self.invoicesButton.grid(column=1,row=1,rowspan=2)    
    
    def invoicesCustomerEditSave(self):
        self.invoices[self.invoicesRowNum][1]=self.customers[int(self.invoicesEditRow.get())-1][0]
        cursor.execute("""
            UPDATE sql5435762.SavedInvoices
            SET Customer='"""+str(self.invoices[self.invoicesRowNum][1]).replace("'", "\\'")+"""'
            WHERE `Invoice Number` ="""+str(self.invoicesNumber)+"""""")
        mydb.commit()   
        self.invoices_df = pd.read_sql_query('SELECT * FROM sql5435762.SavedInvoices',mydb)  # Reset Dataframe to new values
        time.sleep(1)  # Pause screen to show user that information is being saved
        self.invoicesEditEntry()

    def invoicesPurchasingEditSave(self):
        self.invoices[self.invoicesRowNum][3]=purchasing
        cursor.execute("""
                UPDATE sql5435762.SavedInvoices
                SET `Purchasing List`='"""+str(self.invoices[self.invoicesRowNum][3]).replace("'", "\\'")+"""'
                WHERE `Invoice Number` ="""+str(self.invoicesNumber)+"""""")
        mydb.commit()   
        self.invoices_df = pd.read_sql_query('SELECT * FROM sql5435762.SavedInvoices',mydb)  # Reset Dataframe to new values
        time.sleep(1)  # Pause screen to show user that information is being saved
        self.invoicesEditEntry()

    def invoicesPayedEditSave(self):
        self.invoices[self.invoicesRowNum][2]=self.Payed
        cursor.execute("""
                UPDATE sql5435762.SavedInvoices
                SET Payed='"""+self.invoices[self.invoicesRowNum][2]+"""'
                WHERE `Invoice Number` ="""+str(self.invoicesNumber)+"""""")
        mydb.commit()   
        self.invoices_df = pd.read_sql_query('SELECT * FROM sql5435762.SavedInvoices',mydb)  # Reset Dataframe to new values
        time.sleep(1)  # Pause screen to show user that information is being saved
        self.invoicesEditEntry()  # Go back to original editing screen

    def invoicesView(self):
        self.NewScreen()
        self.invoicesDisplay=scrolledtext.ScrolledText(width=200,height=55,font=("Arial",10))
        self.invoicesDisplay.grid(columnspan=5,row=0)
        if len(self.invoices)==0:  # If nothing in invoices list(No invoices added or in database)
            self.invoicesDisplay.insert(tk.INSERT,"No Invoices Saved")
        else:  
            self.invoicesDisplay.insert(tk.INSERT,self.invoices_df.to_string(index=False,justify="right",col_space=25))
        self.back=tk.Button(text="Back",font=("Arial",20),width=90,height=4, command=lambda: self.invoicesHome())
        self.back.grid(row=1,columnspan=5)  

    def invoicesDelete(self):
        self.NewScreen()
        self.deleteDisplay=scrolledtext.ScrolledText(width=130,height=55,font=("Arial",10))
        self.deleteDisplay.grid(column=0,row=0)
        self.back=tk.Button(text="Back",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesHome())
        self.back.grid(column=0,row=1)
        if len(self.invoices)==0:  # If nothing in invoices list(No invoices added or in database)
            self.deleteDisplay.insert(tk.INSERT,"No Invoices Saved")
        else:  
            self.deleteDisplay.insert(tk.INSERT,self.invoices_df.to_string(index=False,justify="right",col_space=25))
        self.deleteChoose=tk.Label(text="Enter Invoice Number to Delete",font=("Arial",20),width=50,height=1)
        self.deleteChoose.grid(column=1,row=0)
        self.deleteEnter=tk.Entry(font=("Arial",20))
        self.deleteEnter.grid(column=1,row=0,rowspan=2)
        self.deleteButton=tk.Button(text="Confirm",font=("Arial",20),width=50,height=4, command=lambda: self.invoicesDeleteSave())
        self.deleteButton.grid(column=1,row=1,rowspan=2)
    
    def invoicesDeleteSave(self):
        deleteRow=int(self.deleteEnter.get())  # Invoice number to delete (Used for MySQL updating)
        if deleteRow>self.invoiceNum or deleteRow<=0:  # If invoice number provided is out of bounds
            self.invoicesDelete()  # Reset page
        else:
            for i in range(len(self.invoices)):  # Changing self.invoicesRowNum from the invoice number the user provided to the actual row number to use for the invoices list
                if self.invoices[i][0]==deleteRow:
                    self.invoicesRowNum=i
            self.invoices.pop(self.invoicesRowNum)  # Delete row using row number
            cursor.execute("""
                DELETE FROM sql5435762.SavedInvoices
                WHERE `Invoice Number` ="""+str(deleteRow)+"""""")
            mydb.commit()      
            self.invoices_df = pd.read_sql_query('SELECT * FROM sql5435762.SavedInvoices',mydb)  # Reset Dataframe to new values
            self.invoicesDelete()  # Reset page to also reset the textbox of invoices
        time.sleep(1)  # Freeze page to show user information is being saved       



class GUI(Products,Customers,Purchasing,Invoices): # Class to incorporate all 4 functions of program and the creation of the GUI class
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


# Setup for GUI and executing it
window=tk.Tk()   
window.title("Business App")
window.geometry("2560x1440")
run=GUI()
window.columnconfigure([0,1,2,3,4,5,6],weight=1)
window.rowconfigure([0,1,2,3,4,5,6],weight=1)
window.mainloop()     

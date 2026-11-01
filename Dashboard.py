import os
import time
from tkinter import*
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
#from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3 
from tkinter import messagebox

class IMS:


    def __init__(self,root):
        self.root=root
        self.root.geometry("1550x820+0+0")
        self.root.title("StoreCore System")
        self.root.config(bg="white")

        '''======title======'''
        self.icon_title=PhotoImage(file="Images/logo1.png")
        title=Label(self.root,text="StoreCore System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#0a1342",fg="white",anchor='w',padx=20).place(x=0,y=0,relwidth=1,height=70)
   
        '''===btn_logout==='''
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1370,y=10,height=50,width=150)
        '''===clock==='''
        self.lbl_clock=Label(self.root,text="Welcome to StoreCore System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4D636D",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        '''===LEFT MENUE==='''
        self.MenuLogo=Image.open("Images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=500)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="White",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="White",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        #btn_Category=Button(LeftMenu,text="Catagory",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="White",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_Products=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="White",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_Sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="White",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_Exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="White",bd=3,cursor="hand2").pack(side=TOP,fill=X)


        '''====Contant===='''
        self.lbl_employee=Label(self.root,text="Total Employee\n[0]",bd=5,relief=RIDGE,bg="#e15e40",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)
        
        self.lbl_supplier=Label(self.root,text="Total Supplier\n[0]",bd=5,relief=RIDGE,bg="#60e140",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)
        
        self.lbl_category=Label(self.root,text="Total Category\n[0]",bd=5,relief=RIDGE,bg="#f21515",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total product\n[0]",bd=5,relief=RIDGE,bg="#fcd708",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[0]",bd=5,relief=RIDGE,bg="#4b0e36",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)
                                 



        '''===Footer==='''
        lbl_footer=Label(self.root,text="SCS- StoreCore system \nFor Any technical issue Contact: 9260923671 ",font=("times new roman",12),bg="#4D636D",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()

#=========================================================================================================================================================================================================================================================================================== 
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)


    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    #def category(self):
       # self.new_win=Toplevel(self.root)
       # self.new_obj=categoryClass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Product\n[{str(len(product))}]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Supplier\n[{str(len(supplier))}]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Category\n[{str(len(category))}]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee\n[{str(len(employee))}]')
            os.makedirs('bill', exist_ok=True)
            bill=len(os.listdir('bill'))    

            self.lbl_sales.config(text=f'Total Sales\n[{str(bill)}]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to StoreCore System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")          



if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()

 
       
 

 
        
        
    

  
     
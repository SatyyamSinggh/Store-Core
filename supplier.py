from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
  
    def __init__(self,root):
        self.root=root
        self.root.geometry("1325x650+200+130")
        self.root.title("StoreCore System")
        self.root.config(bg="white")
        self.root.focus_force()
#======================================================================
        ##===All variables=== 
        self.var_searchby=StringVar()
        
        
        self.var_sup_invoice=StringVar()
        self.var_sup_name=StringVar()
        self.var_contact=StringVar()

        self.var_searchtxt=StringVar()

        self.var_cat_id=StringVar()
        self.var_cat_name=StringVar()



       ##====optionbox=== 
        lbl_search=Label(self.root,text="Search By Invoice No.",bg="white",font=("times new roman",15))
        lbl_search.place(x=700,y=60)
        
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=890,y=60)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15),bg="#76c64d",fg="white",cursor="hand2").place(x=1110,y=59,width=150,height=28)

       ##====title==== 
        title=Label(self.root,text="Supplier Details",font=("goudy old style", 15,"bold"),bg="#184a45",fg="White",bd=3,relief=RIDGE).place(x=50,y=5,width=1210,height=30)

        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",15,"bold"),bg="#184a45",fg="white",bd=3,relief=RIDGE).place(x=50,y=350,width=1210,height=30)
        
        #=============content===================== 
       ##===row1=== 
        lbl_supplier_invoice=Label(self.root,text="Invoice no.",font=("goudy old style", 15,"bold"),bg="White").place(x=50,y=60 )
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style", 15),bg="lightyellow").place(x=165,y=60,width=180 )
       
       
       ##===row2=== 
        lbl_name=Label(self.root,text="Name",font=("goudy old style", 15,"bold"),bg="White").place(x=50,y=100 ) 
        txt_name=Entry(self.root,textvariable=self.var_sup_name,font=("goudy old style", 15),bg="lightyellow").place(x=165,y=100,width=180 )

       ##===row3=== 
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style", 15,"bold"),bg="White").place(x=50,y=140 )
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style", 15),bg="lightyellow").place(x=165,y=140,width=180 )
        
       
       ##===row4===
        lbl_desc=Label(self.root,text="Description",font=("goudy old style", 15,"bold"),bg="White").place(x=50,y=180 )
        self.txt_desc=Text(self.root,font=("goudy old style", 15),bg="lightyellow")
        self.txt_desc.place(x=165,y=180,width=485,height=100)
        
        #=======row5=====================
        lbl_name=Label(self.root,text="Manage Product Category : ",font=("goudy old style",15,"bold"),bg="#ffffff").place(x=50,y=390)
        lbl_name=Entry(self.root,textvariable=self.var_cat_name,font=("goudy old style",15),bg="lightyellow").place(x=165,y=430,width=235)

        lbl_add=Button(self.root,text="ADD",command=self.add_category,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=415,y=430,width=110,height=28)
        lbl_delete=Button(self.root,text="Delete",command=self.delete_category,font=("goudy old style",15),bg="#ff0000",fg="white",cursor="hand2").place(x=540,y=430,width=110,height=28)
        
       ##===button=== 
        btn_add=Button(self.root,text="Save",command=self.add_supplier,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=165,y=300,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update_supplier,font=("goudy old style",15),bg="#068511",fg="white",cursor="hand2").place(x=290,y=300,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete_supplier,font=("goudy old style",15),bg="#e73737",fg="white",cursor="hand2").place(x=415,y=300,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#737692",fg="white",cursor="hand2").place(x=540,y=300,width=110,height=28)
 



       ##===Supplier Details===##
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=100,width=560,height=230)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        

        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")

        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_supplier_data)
        self.show_supplier()

          #=========================================================Catogory Details=================================================================

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=400,width=560,height=200)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)
        

        self.categoryTable.heading("cid",text="C ID")
        self.categoryTable.heading("name",text="Name")
        self.categoryTable["show"]="headings"
        self.categoryTable.column("cid",width=90)
        self.categoryTable.column("name",width=100)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.get_category_data)

        self.show_category()
    


#===========================================================================================================================

    def add_supplier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be required",parent=self.root)

            elif self.var_contact.get()=="":
                messagebox.showerror("Error","Contact Must be required",parent=self.root)

            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice no. already assigned, try different",parent=self.root)
                else: 
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                           self.var_sup_invoice.get(),
                                           self.var_sup_name.get(),                                        
                                           self.var_contact.get(),
                                           self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Addedd Successfully",parent=self.root)
                    self.show_supplier()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def show_supplier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from Supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def get_supplier_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0])
        self.var_sup_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),
        

    def update_supplier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","invoice no. must be required",parent=self.root)

            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else: 
                    cur.execute("Update Supplier set name=?,contact=?,desc=? where invoice=?",(
                                           
                                            self.var_sup_name.get(),
                                            self.var_contact.get(), 
                                            self.txt_desc.get('1.0',END),
                                            self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                    self.show_supplier()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def delete_supplier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be required",parent=self.root)

            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_sup_name.set("")       
        self.var_contact.set("")    
        self.txt_desc.delete('1.0',END),        
        self.var_searchtxt.set("")       
        self.show_supplier()

    def search (self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
             
            if self.var_searchtxt.get()=="":
               messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
               
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())                  
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        #self.show_supplier()    
    #===========================================================================================================================================
      
 #======================================================================================================
    def add_category(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_name.get()=="":
                messagebox.showerror("Error","Category name should be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_cat_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present, try different",parent=self.root)
                else: 
                    cur.execute("Insert into category(name) values(?)",(self.var_cat_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Addedd Successfully",parent=self.root)
                    self.show_category()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show_category(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_category_data(self,ev):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_cat_name.set(row[1])

    def delete_category(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","select category from the list",parent=self.root)

            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show_category()
                        self.var_cat_id.set("")
                        self.var_cat_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)  
           

if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()

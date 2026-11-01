import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import email_pass
import smtplib
import time
class login_system:
    def __init__(self):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1550x820+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''
        #===================images=========================
        #self.phone_image=ImageTk.PhotoImage(Image.open("Images/login.jpeg"))
        #self.lbl_phone_image=Label(self.root,image=self.phone_image)
        #self.lbl_phone_image.place(x=1,y=1,width=1800,height=820)
        win_w, win_h = 1550, 820
        self.root.geometry(f"{win_w}x{win_h}+0+0")
        img = Image.open("Images/login.jpg").resize((win_w, win_h), Image.LANCZOS)
        self.phone_image = ImageTk.PhotoImage(img)
        self.lbl_phone_image = Label(self.root, image=self.phone_image)
        self.lbl_phone_image.place(x=0, y=0, width=win_w, height=win_h)

        #===================login frame=========================
        self.employee_id=StringVar()
        self.password=StringVar()

        self.login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        self.login_frame.place(x=600,y=150,width=350,height=460)

        title=Label(self.login_frame,text="Login Here",font=("Elephant",30,"bold"),bg="white",fg="black")
        title.place(x=0,y=30,relwidth=1)

        lbl_user=Label(self.login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171")
        lbl_user.place(x=50,y=100)

        text_user=Entry(self.login_frame,font=("times new roman",15),bg="#ECECEC",textvariable=self.employee_id)
        text_user.place(x=50,y=140,width=250)

        lbl_pass=Label(self.login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171")
        lbl_pass.place(x=50,y=200)
        text_pass=Entry(self.login_frame,show="*",font=("times new roman",15),bg="#ECECEC",textvariable=self.password)
        text_pass.place(x=50,y=240,width=250)

        btn_login=Button(self.login_frame,text="Login",font=("arial rounded mt bold",15),bg="#00B0F0",fg="white",cursor="hand2",command=self.login)
        btn_login.place(x=50,y=300,width=250,height=35)

        hr=Label(self.login_frame,bg="lightgray")
        hr.place(x=50,y=370,width=250,height=2)

        or_=Label(self.login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold"))
        or_.place(x=150,y=355)

        btn_forget=Button(self.login_frame,text="Forget Password?",font=("times new roman",13),bg="white",fg="#00759E",bd=0,cursor="hand2",command=self.forget_window)
        btn_forget.place(x=100,y=390)

    def login(self):
       conn=sqlite3.connect(database=r'ims.db')
       cur=conn.cursor()
       try:
           if self.employee_id.get()=="" or self.password.get()=="":
               messagebox.showerror("Error","All fields are required",parent=self.root)
           else:    
                cur.execute("select utype from employee where eid=? and pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid USERNAME & PASSWORD",parent=self.root)
                else:
                   if user[0]=="Admin":
                        messagebox.showinfo("Success","Welcome to Admin Panel",parent=self.root)
                        self.root.destroy()
                        os.system("python dashboard.py") 
                   else:
                        messagebox.showinfo("Success","Welcome to Billing Panel",parent=self.root)
                        self.root.destroy()
                        os.system("python billing.py")      
       except Exception as ex:
           messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)   

#=====================forget password window=========================
    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                 messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email == None:
                   messagebox.showerror("Error","Invalid Employee ID, try again",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    chk=self.send_email(email[0])
                    if chk!='s':
                        messagebox.showerror("Error","Connection Error, try again",parent=self.root)
                    else:
                        self.foreget_win=Toplevel(self.root)
                        self.foreget_win.title("Reset Password")
                        self.foreget_win.geometry("400x380+500+100")
                        self.foreget_win.focus_force()

                        title=Label(self.foreget_win,text="Reset Password",font=("goudy old style",20,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.foreget_win,text="Enter OTP Sent to your email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.foreget_win,font=("times new roman",15),bg="lightyellow",textvariable=self.var_otp).place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.foreget_win,text="Submit",command=self.validate_otp,font=("times new roman",15),bg="#1CD2B1",fg="white",cursor="hand2")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)
                        

                        lbl_new_pass=Label(self.foreget_win,text="Enter New Password",font=("times new roman",15)).place(x=20,y=140)
                        txt_new_pass=Entry(self.foreget_win,font=("times new roman",15),bg="lightyellow",textvariable=self.var_new_pass).place(x=20,y=180,width=250,height=30)

                        lbl_conf_pass=Label(self.foreget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=220)
                        txt_conf_pass=Entry(self.foreget_win,font=("times new roman",15),bg="lightyellow",textvariable=self.var_conf_pass).place(x=20,y=260,width=250,height=30)

                        self.btn_update=Button(self.foreget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2")
                        self.btn_update.place(x=150,y=320,width=100,height=30)
                                            
                   
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.foreget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","Password Mismatch",parent=self.foreget_win)
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("update employee set pass=? where eid=?", (self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password Updated Successfully",parent=self.foreget_win)
                self.foreget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.foreget_win)    
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, try again",parent=self.foreget_win) 


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_
        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))

        subject="IMS-Reset Password OTP"
        msg=f'Dear Sir/Madam,\n\nYour OTP for Reset Password is {str(self.otp)}.\n\nThanks & Regards,\nIMS Team'
        msg="Subject:{}\n\n{}".format(subject,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'


root=Tk()
obj=login_system()
root.mainloop()    
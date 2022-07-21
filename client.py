from ast import arg
from http import client
from itertools import count
import socket
import json
from email import message
import tkinter as tk
from tkinter import VERTICAL, Canvas, Frame, Label, Scrollbar, Widget, ttk,Spinbox
from turtle import width
from PIL import ImageTk, Image
import os
from functools import partial
import array as arr
import shutil
from tkinter.messagebox import showinfo
from time import sleep
from numpy import full
from datetime import datetime, date, timedelta

IP = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf8"
SIZE = 1024
DISCONNECTMES = "Disconnect"
 
#Xuat anh ra man hinh(khong quan trong lam vi no la front end)
def Print_Pic(mes, data):
    image = []
    img = []
    my_img = []
    w = []
    #create frame
    my_pic = Frame(mes, width= 700, height=400)
    my_pic.grid()
    #create canvas
    my_canvas = Canvas(my_pic, width= 700, height=400)
    my_canvas.grid(row = 1, column = 0)
    scrollbar = ttk.Scrollbar(my_pic, orient= VERTICAL, command= my_canvas.yview)
    scrollbar.grid(column = 1, row = 1)
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    frame = Frame(my_canvas, width= 700, height= 400)
    my_canvas.create_window((700,400),window=frame, anchor='nw')
    for i in data:
        image.append(Image.open(i['Picture']))
    for i in range(0, len(data)):
        img.append(image[i].resize((200, 120)))
        my_img.append(ImageTk.PhotoImage(img[i]))
        w.append(tk.Label(frame, image=my_img[i]))
        w[i].grid(row = int(i  / 3) * 2, column =  int((i+ 1) % 3), ipadx = 20, ipady = 20)
        tk.Label(frame, text ='NameFood: ' + data[i]['NameFood'] + '\n Price: ' + data[i]['Price'] + '\n Note: ' + data[i]['Note'], font = 'TimeNewRoman').grid(row = int(i  / 3)*2 + 1, column =  int((i+ 1) % 3), ipadx = 20, ipady = 20)
    #
    mes.mainloop()
  
def Do_when_press_x_in_menu(frame): 
    dir_path = "./Menu"
    shutil.rmtree(dir_path, ignore_errors=True)
    frame.destroy()

def Do_when_press_x_in_order_new(frame, client, ms):
    client.send("Out_x".encode(FORMAT))
    ms.counter = 0
    frame.destroy()
    
def Do_when_press_x_in_order_update(frame, client, ms):
    client.send("Out_x".encode(FORMAT))
    frame.destroy()
    
def Do_when_press_x_in_pay(frame, client, ms):
    client.send("Out_x".encode(FORMAT))
    frame.destroy()
    
def Do_when_press_x_in_main(client, ms):
    client.send("Out_x".encode(FORMAT))
    sleep(1)
    ms.destroy()

#menu button
def Menu_button(client):
    #send and create window
    client.send('Menu'.encode(FORMAT))
    menu = tk.Toplevel()
    menu.title('Menu')
    window_width = 800
    window_height = 600
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    menu.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    menu.resizable(False,False)
    menu.attributes('-topmost',1)
    #
    menusage = tk.Label(menu,text='MENU', font = 'TimeNewRoman')
    menusage.grid(column = 0, row = 0, sticky= 'n')
    #Nhan data menu.json tu server
    data = json.loads(client.recv(SIZE).decode(FORMAT))
    #Tao folder Menu de chua anh(picture)
    isdir = os.path.isdir('Menu')
    if (isdir == False):
        os.mkdir('Menu')
    #bien dem mang list(cac phan tu trong file menu.json)
    count = len(data)
    x = 0 #variable to count in loop
    #loop for receive picture
    while x < count:
        size_file = client.recv(SIZE)
        client.send('size'.encode(FORMAT))
        size_file = int(size_file)
        picture = open(data[x]['Picture'], 'wb')
        current_size = 0
        image_chunk = client.recv(1024*10)
        while image_chunk:
            current_size += len(image_chunk)
            picture.write(image_chunk)
            if current_size == size_file:
                break
            image_chunk = client.recv(1024*10)
        picture.close()
        client.send('full'.encode(FORMAT))
        x += 1
    #ending of loop in receive picture
    Print_Pic(menu, data)
    menu.protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_menu, menu))
    menu.mainloop()
#


#Order_button    
   #New order button
def Order_Food(client, ms):
    client.send('Order'.encode(FORMAT))
    data = json.loads(client.recv(SIZE).decode(FORMAT))
    order = tk.Toplevel()
    order.title('Client')
    window_width = 800
    window_height = 600
    screen_width = order.winfo_screenwidth()
    screen_height = order.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    order.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    order.resizable(False,False)
    order.attributes('-topmost',1)
    title = tk.Label(order,text='ORDER', font = 'TimeNewRoman')
    title.grid(row = 0, ipadx = 350, ipady = 80)
    button1 = tk.Button(order, text = 'New Order', font = 'TimeNewRoman', command=partial(New_List_Food, client, order, data, ms))
    button2 = tk.Button(order, text = 'Update Order', font = 'TimeNewRoman', command = partial(Update_List_Food, client, order, data, ms))
    button1.grid(row = 1, pady = 30, ipadx = 20)
    button2.grid(row = 2, pady = 30, ipadx = 20)
    order.protocol('WM_DELETE_WINDOW',partial(Do_when_press_x_in_order_update, order, client, ms))
    #run Do_when_press_x_in_order_update vi no khong xoa bien counter
    order.mainloop
    
    
def New_List_Food(client, order, data, ms):
    #destroy screen before
    client.send("new_amount_food".encode(FORMAT))
    if (ms.counter >= 1):
        client.send('Extra_order'.encode(FORMAT))
        order.destroy()
        tk.messagebox.showinfo(title='Warning',message='Da co don hang va khong the dat them')
        return
    ms.counter = ms.counter + 1
    order.destroy() 
    #create new window
    dish_order = tk.Toplevel()
    dish_order.title('Client')
    window_width = 800
    window_height = 600
    screen_width = dish_order.winfo_screenwidth()
    screen_height = dish_order.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    dish_order.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    dish_order.resizable(False,False)
    dish_order.attributes('-topmost',1)
    #
    tittle = tk.Label(dish_order, text = 'New Order', font = 'TimeNewRoman')
    tittle.grid(row = 0, column = 0, sticky='ne')
    tittlefood = tk.Label(dish_order, text = 'DISHES', font = 'TimeNewRoman')
    tittlefood.grid(row =1 , column = 0, sticky= 'nw')
    my_food = Frame(dish_order, width= 450, height=400)
    my_food.grid()
    #create canvas
    my_canvas = Canvas(my_food, width= 450, height=400)
    my_canvas.grid(row = 2, column = 0, sticky = 'w')
    scrollbar = ttk.Scrollbar(my_food, orient= VERTICAL, command= my_canvas.yview)
    scrollbar.grid(column = 2, row = 2, sticky='e')
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    frame = Frame(my_canvas, width= 450, height= 400)
    my_canvas.create_window((450,400),window=frame, anchor='nw')
    list_food = []
    valuecheck = []
    for i in range(0,len(data)):
        valuecheck.append(tk.IntVar())
        ttk.Checkbutton(frame, text = data[i]['NameFood'], onvalue=1, offvalue=0, variable=valuecheck[i]).grid(column = 0 , row = i + 2, sticky='w' )
    tk.Button(dish_order, text = "Input amount of dishes", font = 'TimeNewRoman',command = partial(New_Next_amount, client, data, dish_order, list_food, valuecheck, ms)).grid(row = 3, column = 2)
    dish_order.protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_order_new, dish_order, client, ms))
 
    
def New_Next_amount(client, data, dish_order, list_food, valuecheck, ms):
    dish_order.destroy()
    send_order = tk.Toplevel()
    send_order.title('Client')
    window_width = 800
    window_height = 600
    screen_width = send_order.winfo_screenwidth()
    screen_height = send_order.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    send_order.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    send_order.resizable(False,False)
    send_order.attributes('-topmost',1)
    for i in range(len(data)):
        if valuecheck[i].get() == 1:
            list_food.append(data[i]['NameFood'])
    tittle = tk.Label(send_order, text = 'New Order', font = 'TimeNewRoman')
    tittle.grid(row = 0, column = 0, sticky='ne')
    tittlefood = tk.Label(send_order, text = 'AMOUNT', font = 'TimeNewRoman')
    tittlefood.grid(row =1 , column = 0, sticky= 'nw')
    #
    my_amount = Frame(send_order, width= 450, height=400)
    my_amount.grid()
    #create canvas
    my_canvas = Canvas(my_amount, width= 450, height=400)
    my_canvas.grid(row = 2, column = 0, sticky = 'w')
    scrollbar = ttk.Scrollbar(my_amount, orient= VERTICAL, command= my_canvas.yview)
    scrollbar.grid(column = 2, row = 2, sticky='e')
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    frame = Frame(my_canvas, width= 450, height= 400)
    my_canvas.create_window((450,400),window=frame, anchor='nw')
    #
    amount = []
    for i in range(0,len(list_food)):
       amount.append(tk.IntVar())
       ttk.Label(frame, text = list_food[i], font='TimeNewRoman').grid(column=0, row = i)
       ttk.Spinbox (frame,from_=1,to=500,textvariable=amount[i],wrap=True).grid(column = 1, row = i)
    tk.Button(send_order, text = "Order", font = 'TimeNewRoman',command = partial(New_Send_order, client, send_order,  list_food, amount)).grid(row = 3, column = 2)
    send_order.protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_order_new, send_order, client, ms))
    send_order.mainloop()
   
    
def New_Send_order(client, send_order, list_food, amount):
    client.send('Send'.encode(FORMAT))
    sleep(0.1)
    client.send(str(list_food).encode(FORMAT))
    for i in range(len(amount)):
        amount[i] = amount[i].get()
    client.send(str(amount).encode(FORMAT))
    tk.messagebox.showinfo(title='Total Payment',message='Order success')
    send_order.destroy()

################################################3
#update button

def Update_List_Food(client, order, data, ms):
    client.send("update_food".encode(FORMAT))
    if (ms.counter <= 0):
        client.send('Not_order'.encode(FORMAT))
        order.destroy()
        tk.messagebox.showinfo(title='Warning',message='Khong co don hang de cap nhat')
        return
    else:
        client.send('Available'.encode(FORMAT))
    now = datetime.now()
    current_time = now.time()
    order_time = client.recv(SIZE).decode(FORMAT)
    print (order_time)
    order_time = datetime.strptime(order_time, "%H:%M:%S").time()
    limit =  timedelta(hours=2)
    t1 = timedelta(hours=order_time.hour, minutes=order_time.minute, seconds=order_time.second)
    t2 = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
    duration = t2 - t1
    print(current_time)
    if  duration >= limit:
        client.send('Over_time'.encode(FORMAT))
        order.destroy()
        tk.messagebox.showinfo(title='Warning',message='Qua thoi gian')
        return
    ms.counter = ms.counter + 1
    order.destroy() 
    #create new window
    dish_order = tk.Toplevel()
    dish_order.title('Client')
    window_width = 800
    window_height = 600
    screen_width = dish_order.winfo_screenwidth()
    screen_height = dish_order.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    dish_order.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    dish_order.resizable(False,False)
    dish_order.attributes('-topmost',1)
    #
    tittle = tk.Label(dish_order, text = 'New Order', font = 'TimeNewRoman')
    tittle.grid(row = 0, column = 0, sticky='ne')
    tittlefood = tk.Label(dish_order, text = 'DISHES', font = 'TimeNewRoman')
    tittlefood.grid(row =1 , column = 0, sticky= 'nw')
    my_food = Frame(dish_order, width= 450, height=400)
    my_food.grid()
    #create canvas
    my_canvas = Canvas(my_food, width= 450, height=400)
    my_canvas.grid(row = 2, column = 0, sticky = 'w')
    scrollbar = ttk.Scrollbar(my_food, orient= VERTICAL, command= my_canvas.yview)
    scrollbar.grid(column = 2, row = 2, sticky='e')
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    frame = Frame(my_canvas, width= 450, height= 400)
    my_canvas.create_window((450,400),window=frame, anchor='nw')
    list_food = []
    valuecheck = []
    for i in range(0,len(data)):
        valuecheck.append(tk.IntVar())
        ttk.Checkbutton(frame, text = data[i]['NameFood'], onvalue=1, offvalue=0, variable=valuecheck[i]).grid(column = 0 , row = i + 2, sticky='w' )
    tk.Button(dish_order, text = "Input amount of dishes", font = 'TimeNewRoman',command = partial(Update_Next_amount, client, data, dish_order, list_food, valuecheck, ms)).grid(row = 3, column = 2)
    dish_order.protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_order_update, dish_order, client, ms))
    dish_order.mainloop()


def Update_Next_amount(client, data, dish_order, list_food, valuecheck, ms):
    dish_order.destroy()
    sendup_order = tk.Toplevel()
    sendup_order.title('Client')
    window_width = 800
    window_height = 600
    screen_width = sendup_order.winfo_screenwidth()
    screen_height = sendup_order.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    sendup_order.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    sendup_order.resizable(False,False)
    sendup_order.attributes('-topmost',1)
    for i in range(len(data)):
        if valuecheck[i].get() == 1:
            list_food.append(data[i]['NameFood'])
    list_order = eval(client.recv(SIZE).decode(FORMAT))
    client.send("food_complete".encode(FORMAT))
    list_amount = eval(client.recv(SIZE).decode(FORMAT))
    tittle = tk.Label(sendup_order, text = 'New Order', font = 'TimeNewRoman')
    tittle.grid(row = 0, column = 0, sticky='ne')
    tittlefood = tk.Label(sendup_order, text = 'AMOUNT', font = 'TimeNewRoman')
    tittlefood.grid(row =1 , column = 0, sticky= 'nw')
    #
    my_amount = Frame(sendup_order, width= 450, height=400)
    my_amount.grid()
    #create canvas
    my_canvas = Canvas(my_amount, width= 450, height=400)
    my_canvas.grid(row = 2, column = 0, sticky = 'w')
    scrollbar = ttk.Scrollbar(my_amount, orient= VERTICAL, command= my_canvas.yview)
    scrollbar.grid(column = 2, row = 2, sticky='e')
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    frame = Frame(my_canvas, width= 450, height= 400)
    my_canvas.create_window((450,400),window=frame, anchor='nw')
    #
    amount = []
    for i in range(0,len(list_food)):
       amount.append(tk.IntVar())
       ttk.Label(frame, text = list_food[i], font='TimeNewRoman').grid(column=0, row = i)
       ttk.Spinbox (frame,from_=1,to=500,textvariable=amount[i],wrap=True).grid(column = 1, row = i)
    tk.Button(sendup_order, text = "Order", font = 'TimeNewRoman',command = partial(Update_Send_order, client, sendup_order,  list_food, amount, list_order, list_amount)).grid(row = 3, column = 2)
    sendup_order.protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_order_update, sendup_order , client, ms))
    sendup_order.mainloop()
     

def Update_Send_order(client, send_order, list_food, amount, list_order, list_amount):
    #list_food, amount is a data that add to old data
    #list_orderm, list_amount is a old data
    client.send('Send'.encode(FORMAT))
    for i in range(len(amount)):
        amount[i] = amount[i].get()
    for i in range(len(list_order)):
        for j in range(len(list_food)):
            if list_order[i] == list_food[j]:
                list_food[j] = 0
                list_amount[i] = list_amount[i] + amount[j]
                amount[j] = 0
    list_food = [i for i in list_food if i != 0]
    amount = [i for i in amount if i != 0]
    print(list_food)
    print(amount)
    list_order.extend(list_food)
    list_amount.extend(amount)
    print(list_order)
    print(list_amount)
    client.send(str(list_order).encode(FORMAT))
    rep_food = client.recv(SIZE).decode(FORMAT)
    if  rep_food == "food_success":  
        client.send(str(list_amount).encode(FORMAT))
    tk.messagebox.showinfo(title='Total Payment',message='Update success')  
    send_order.destroy()  
    

#################################################
#Pay button
def Pay_food(client, ms):
    #send pay to the server to know the mode
    client.send('Pay'.encode(FORMAT))
    reply = client.recv(SIZE).decode(FORMAT)
    #du lieu se la "Not pay" neu ko co don hang thanh toan
    #du lieu se la money cua don hang neu co don can thanh toan.
    if reply == "Not_pay":
        tk.messagebox.showinfo(title='Anouncement',message='No order to pay')
        return
    else: 
        money = json.loads(reply)
    #tao window o che do pay
    pay = tk.Toplevel()
    pay.title('Client')
    window_width = 800
    window_height = 600
    screen_width = pay.winfo_screenwidth()
    screen_height = pay.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    pay.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    pay.resizable(False,False)
    pay.attributes('-topmost',1)
    #
    tk.Label(pay,text='PAY', font = ('TimeNewRoman', 20)).grid(column=0, row = 0, sticky='n', padx= 150)
    #in ra man hinh tin va tien them
    tk.Label(pay,text="Your bill is " + str(money[0]) + "+ " + str(money[1] - money[0]) +" money you adding", font = ('TimeNewRoman', 25)).grid(column=0, row = 1, sticky='n', padx=150)
    #
    #Nut de thnah toan bang tien mat
    button1 = tk.Button(pay, text = 'Pay cash ', font = 'TimeNewRoman',command=partial(Pay_Success, ms, client, pay)).grid(row = 2, pady = 30, ipadx = 20)
    #nut de thanh toan bang the ATM
    button2 = tk.Button(pay, text = 'Use credit card for payment ', font = 'TimeNewRoman', command=partial(Check_CD, ms, client, pay)).grid(row = 3, pady = 30, ipadx = 20)
    #thuc hien khi an nut X
    pay.wm_protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_pay, pay, client, ms))


def Pay_Success(ms, client, frame):
    ms.counter = 0
    #thanh toan thanh cong, bien dem don hang ve lai 0
    client.send('Pay_Success'.encode(FORMAT))
    # gui cho server 
    tk.messagebox.showinfo(title='Anouncement',message='Payment success')
    #huy cua so
    frame.destroy()

#Ham kiem tra xem so the co phu hop khong
def Do_when_pay_CD(ms, client, data, frame):
    num = data.get(1.0, "end-1c")
    if num.isdigit():
        num = int(num)
        #so co 10 chu so 
        if num >= 1000000000 and num <= 9999999999:
            Pay_Success(ms, client, frame)
            tk.messagebox.showinfo(title='Total Payment',message='This number of credit card is correct and paying bill successfull')
            frame.destroy()
        else:
            #sai yeu cau so
            tk.messagebox.showinfo(title='Total Payment',message='Syntax or number is not correct')
            frame.attributes('-topmost',True)
    else :
        #co chu
        tk.messagebox.showinfo(title='Total Payment',message='Syntax or number is not correct')
        frame.attributes('-topmost',True)


def Check_CD(ms, client, frame):
    frame.destroy()
    #tao cua so input so the
    cd = tk.Toplevel()
    cd.title('Client')
    window_width = 800
    window_height = 600
    screen_width = cd.winfo_screenwidth()
    screen_height = cd.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    cd.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    cd.resizable(False,False)
    cd.attributes('-topmost',1)
    #
    ttk.Label(cd, text='PAY BY CREDIT CARD', font = ('TimeNewRoman', 20)).grid(column=0, row = 0, sticky='n', padx= 200)
    ttk.Label(cd, text='Input number of credit card in this text box', font = ('TimeNewRoman', 20)).grid(column=0, row = 1, sticky='n', padx= 50)
    inputtxt = tk.Text(cd, height = 5, width = 25, bg = "light yellow")
    inputtxt.grid(column = 0, row = 2)
    #button de xac nhan gui thanh toan
    ttk.Button(cd ,text='Click here to pay', command = partial(Do_when_pay_CD, ms, client, inputtxt, cd)).grid(column=0, row = 3, sticky='n', padx= 200)
    cd.wm_protocol('WM_DELETE_WINDOW', partial(Do_when_press_x_in_pay, cd, client, ms))

##########################33
#quit button

def Quit_button(client, ms):
    client.send('Quit'.encode(FORMAT))
    rep = client.recv(SIZE).decode(FORMAT)
    if rep == "Have_order":
        tk.messagebox.showinfo(title='Announcement',message='You have a order to pay, please pay')
        pass
        return
    else:
        dir_path = "./Menu"
        shutil.rmtree(dir_path, ignore_errors=True)
        client.send('Quit'.encode(FORMAT))
        ms.destroy()  

##################################
#main screen
def mainscreen(client):
    #create window
    ms = tk.Tk()
    ms.title('Client')
    window_width = 800
    window_height = 600
    screen_width = ms.winfo_screenwidth()
    screen_height = ms.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    ms.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    ms.resizable(False,False)
    ms.attributes('-topmost',1)
    ms.counter = 0#counter to count the order in this computer
    #create button with 4 option
    messege = tk.Label(ms, text = "OPTION",  font = 'TimeNewRoman')
    messege.grid(ipady=80, ipadx = 350, column= 1, row = 0)
    #menu button
    button1 = ttk.Button(ms, text= "MENU",command=partial(Menu_button, client ))
    button1.grid(ipady=10, column= 1, row = 1)
    # order button
    button2 = ttk.Button(ms, text="ORDER",command=partial(Order_Food, client, ms))
    button2.grid(ipady=10, column= 1, row = 2)
    #pay button
    button3 = ttk.Button(ms, text="PAY",command=partial(Pay_food, client, ms))
    button3.grid(ipady=10, column= 1, row = 3)
    #quit button
    button4 = ttk.Button(ms, text="QUIT",command=partial(Quit_button, client, ms))
    button4.grid(ipady=10, column= 1, row = 4)
    #
    ms.mainloop()
    #define x button
    ms.wm_protocol('WM_DELETE_WINDOW',Do_when_press_x_in_main(client, ms))

#main function
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, PORT)
    print("Client connect to server with port: " + str(PORT))
    #ket noi den server
    client.connect(server_address)
    mainscreen(client)
    
if __name__ == "__main__":
    main()
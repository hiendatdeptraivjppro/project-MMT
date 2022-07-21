from asyncio.windows_events import NULL
from http import server
from pickle import TRUE
import socket
from tabnanny import check 
import threading
from time import sleep
import tkinter as tk
import json
import os
from datetime import datetime

IP = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf8"
SIZE = 1024
DISCONNECTMES = "Disconnect"



def check_Empty_order(order, t):
    for i in range(0, len(order)):
                if (order[i]["NumberDesk"] == t) and order[i]["Static"] == "No":
                    return False
    return True

def read_in_chunk(file, chunk_size = 1024*10):
    while True:
        chunk = file.read(chunk_size)
        if chunk:
            yield chunk
        else:
            return chunk

def InFile_Menu(file):
    f = open(file, 'r')
    data = ""
    for chunk in read_in_chunk(f):
        data = str(data) + chunk 
    f.close()  
    return str(data)

def OutFIle_Menu(data_output, file):
    f = open(file, 'w')
    f.write(json.dumps(data_output, indent=7))
    f.close()

def One_Price(food):
    data_menu = json.loads(InFile_Menu('menu.json'))
    count = 0
    price = []
    for count in range(len(food)):
        for j in range(len(data_menu)):
            if count == len(food):
                break
            if food[count] == data_menu[j]['NameFood']:
                price.append(data_menu[j]['Price'])
    return price

def Total_Price(one_price, amount):
    sum = 0
    for i in range(len(one_price)):
        sum = int (sum + int(one_price[i]) * int(amount[i]))
    return sum

def handle_client(conn, addr, t):
    print(f"[NEW CONNECTION] {addr} connected \n")
    connect = True
    while connect:
        mes = conn.recv(SIZE).decode(FORMAT)#ham nhan lenh o server
        if mes == 'Menu':
            file = 'menu.json'
            data_menu = InFile_Menu(file)
            dict_data = json.loads(data_menu)
            #count is a number of obj in dictionary
            count = len(dict_data)    
            #gui file menu.json      
            conn.send(data_menu.encode(FORMAT))
            x = 0 #variable to count loop
            check_pic = True #variable to check full pic or not
            #gui anh
            while x < count and check_pic == True:
                check_pic = False
                Image = open(dict_data[x]['Picture'], 'rb')
                filesize = os.path.getsize(dict_data[x]['Picture'])
                conn.send(str(filesize).encode(FORMAT))
                back_size = conn.recv(SIZE).decode(FORMAT)
                if back_size == "size":
                    image_data = Image.read(1024*10)
                    while image_data:
                        conn.send(image_data)
                        image_data = Image.read(1024*10) 
                    Image.close()
                    notice = conn.recv(SIZE).decode(FORMAT)
                    if notice == 'full':
                        check_pic = True
                        x += 1
            ###
        if mes == 'Order':
            file = 'menu.json'
            data_order = InFile_Menu(file)
            dict_data = json.loads(data_order)
            #count is a number of obj in dictionary          
            conn.send(data_order.encode(FORMAT))
            command_order = conn.recv(SIZE).decode(FORMAT)
            if command_order == "new_amount_food":
                checkrep1 = conn.recv(SIZE).decode(FORMAT)
                if checkrep1 == 'Send':
                    food = eval(conn.recv(SIZE).decode(FORMAT))#Nhan list food ben order client gui qua
                    file = 'order.json'
                    order = json.loads(InFile_Menu(file))
                    amount = eval(conn.recv(SIZE).decode(FORMAT))#Nhan list amount ben order client gui qua
                    #set gio dat
                    now = datetime.now()
                    time = now.strftime("%H:%M:%S")
                    #
                    #Tao list de add vao data
                    dict_order = {
                        "NumberDesk" : t,
                        "NameDishes" : food,
                        "AlonePrice" : One_Price(food),
                        "Amount" : amount,
                        "Old Total" : Total_Price(One_Price(food), amount),
                        "Current Total" : Total_Price(One_Price(food), amount),
                        "Time" : time,
                        "Static" : "No"
                    }
                    order.append(dict_order)
                    #Dan vao data(order.json)
                    OutFIle_Menu(order, file)
                if checkrep1 == "Out_x":
                    continue
                if command_order == "extra_order":
                    continue
            if command_order == "update_food":
                checkrep2 = conn.recv(SIZE).decode(FORMAT) 
                file = 'order.json'
                order = json.loads(InFile_Menu(file))
                if checkrep2 == "Not_order" or checkrep2 == "Over_time":
                    continue
                if checkrep2 == "Available":
                    for i in range(0, len(order)):
                            if (order[i]["NumberDesk"] == t) and order[i]["Static"] == "No":
                                #gui thoi gian de check xem co hop le hay khong
                                conn.send(str(order[i]['Time']).encode(FORMAT))
                                sleep(0.5)
                                conn.send(str(order[i]['NameDishes']).encode(FORMAT))
                                rep = conn.recv(SIZE).decode(FORMAT)
                                if rep == "food_complete":
                                    conn.send(str(order[i]['Amount']).encode(FORMAT))
                                break
                    rep_order = conn.recv(SIZE).decode(FORMAT)
                    if rep_order == 'Send':
                        #mo order.json r chinh sua lai don hang da cap nhat
                        file = 'order.json'
                        order = json.loads(InFile_Menu(file))
                        for i in range(0, len(order)):
                            if (order[i]["NumberDesk"] == t) and (order[i]["Static"] == "No"):
                                food = eval(conn.recv(SIZE).decode(FORMAT))
                                print(food)
                                conn.send('food_success'.encode(FORMAT))
                                amount = eval(conn.recv(SIZE).decode(FORMAT))
                                print(amount)
                                order[i] = {
                                "NumberDesk" : t,
                                "NameDishes" : food,
                                "AlonePrice" : One_Price(food),
                                "Amount" : amount,
                                "Old Total" : order[i]["Old Total"],
                                "Current Total": Total_Price(One_Price(food), amount),
                                "Time" : order[i]["Time"],
                                "Static" : "No"
                                }
                                break
                        OutFIle_Menu(order, file)   
                if checkrep2 == "Out_x":
                    continue
            if command_order == "Out_x":
                continue
                #for i in range(0, len(food)):
            if command_order == "Not_order":
                continue
                
        if mes == 'Pay':
            file = 'order.json'
            order = json.loads(InFile_Menu(file))
            if check_Empty_order(order, t):
                conn.send('Not_pay'.encode(FORMAT))
            for i in range(0, len(order)):
                if (order[i]["NumberDesk"] == t) and order[i]["Static"] == "No":
                    list_money = [order[i]['Old Total'], order[i]['Current Total']]
                    #LIST_MONEY WITH LISY_MONEY[0] IS OLD TOTAL(OLD MONEY), MONEY[2] IS CURRENT MONEY
                    conn.send(str(list_money).encode(FORMAT)) 
                    pay_full = conn.recv(SIZE).decode(FORMAT)
                    if pay_full == 'Pay_Success':
                        order[i]["Static"] = "Pay"
                    break
            OutFIle_Menu(order, file)        
        if mes == 'Quit':
            file = 'order.json'
            order = json.loads(InFile_Menu(file))
            if check_Empty_order(order, t): 
                conn.send('Bye'.encode(FORMAT)) 
                connect = False
            else:
                conn.send('Have_order'.encode(FORMAT))
                continue
        if mes == 'Out_x':
            file = 'order.json'
            order = json.loads(InFile_Menu(file))
            for i in range(0, len(order)):
                if (order[i]["NumberDesk"] == t) and order[i]["Static"] == "No":
                    del order[i]
                    break
            connect = False
            OutFIle_Menu(order, file)
        print(mes)
    print(f"[{addr}] {mes}")
    conn.close()
    

############################################
def main(): 
    print("[STARTING] Server is starting ...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tao server
    server.bind((IP, PORT))
    #nghe ip de ket noi
    server.listen()
    print(f"[LISTENING] Server is listening on {IP} : {PORT}")
    while True:
        conn, addr = server.accept()#dong y cho client ket noi
        t = threading.active_count()#dem co bao nhieu ket noi den server
        thread = threading.Thread(target=handle_client, args=(conn, addr, t))#tao mot vung de chay client 
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {t}")

if __name__ == "__main__":
    main()
    
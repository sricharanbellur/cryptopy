from tkinter import *
from tkinter import messagebox,Menu
import requests
import json
import sqlite3

pycrypto  = Tk()
pycrypto.title("My Portfolio")
pycrypto.iconbitmap('favicon.ico')

con =sqlite3.connect('coin.db')
curobj =con.cursor()

curobj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT,amount INTEGER,price  REAL)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    app_nav()
    my_pf()
    app_header()
def app_nav():
    def clear_all():
        curobj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()

    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)

def my_pf():
    api_req=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=4b997c48-539a-4468-8fd0-092c78eae47f")
    api = json.loads(api_req.content)
    
    curobj.execute("SELECT * from coin")
    coins = curobj.fetchall()
    
    def fontcolor(amount):
        if amount>=0:
            return"green"
        else :
            return"red"

    def addcoin():
        curobj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()
        reset()
        messagebox.showinfo("Coin Portfolio MESSAGE!!","Coin Added to the portfolio succesfully.")

    def updatecoin():
        curobj.execute("UPDATE coin SET symbol=?,price=?,amount=? WHERE id =?",(symbol_up.get(),price_up.get(),amount_up.get(),port_idu.get()))
        con.commit()
        reset()
        messagebox.showinfo("Coin Portfolio MESSAGE!!","Coin UPDATED succesfully.")

    def deletecoin():
        curobj.execute("DELETE from coin WHERE id =?",(pfid_del.get(),))
        con.commit()
        reset()
        messagebox.showinfo("Coin Portfolio MESSAGE!!","Coin Deleted from the portfolio succesfully.")

    total_pl=0
    total_cv=0
    total_cp=0
    
    coin_row = 1
    for i in range(0, 300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_cost =coin[2] * coin[3]
                current_cost=coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pr_pc=api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_prc = pr_pc * coin[2]
                
                total_pl += total_prc
                total_cv+=current_cost
                total_cp+=total_cost
                
                pf_id = Label(pycrypto,text=coin[0],bg="white",fg="black",font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                pf_id.grid(row=coin_row,column=0,sticky =N+S+E+W)

                name = Label(pycrypto,text=api["data"][i]["symbol"],bg="white",fg="black",font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                name.grid(row=coin_row,column=1,sticky =N+S+E+W)

                price = Label(pycrypto,text=api["data"][i]["quote"]["USD"]["price"],bg="white",fg="black",font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                price.grid(row=coin_row,column=2,sticky =N+S+E+W)

                no_owned= Label(pycrypto,text=coin[2],bg="white",fg="black",font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                no_owned.grid(row=coin_row,column=3,sticky =N+S+E+W)

                amount_paid = Label(pycrypto,text="${0:.2f}".format(total_cost),bg="white",fg="black",font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                amount_paid.grid(row=coin_row,column=4,sticky =N+S+E+W)

                current_value = Label(pycrypto,text="${0:.2f}".format(current_cost),bg="white",fg="black",font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                current_value.grid(row=coin_row,column=5,sticky =N+S+E+W)

                profit_per_c = Label(pycrypto,text="${0:.2f}".format(pr_pc),bg="white",fg=fontcolor(float("{0:.2f}".format(pr_pc))),font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                profit_per_c.grid(row=coin_row,column=6,sticky =N+S+E+W)

                total_plc = Label(pycrypto,text="${0:.2f}".format(total_prc),bg="white",fg=fontcolor(float("{0:.2f}".format(total_prc))),font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
                total_plc.grid(row=coin_row,column=7,sticky =N+S+E+W)
                
                coin_row+=1
                #insertcoin
    symbol_txt = Entry(pycrypto,borderwidth=2,relief="groove")
    symbol_txt.grid(row=coin_row+1,column=1,sticky =N+S+E+W)

    price_txt = Entry(pycrypto,borderwidth=2,relief="groove")
    price_txt.grid(row=coin_row+1,column=2,sticky =N+S+E+W)

    amount_txt = Entry(pycrypto,borderwidth=2,relief="groove")
    amount_txt.grid(row=coin_row+1,column=3,sticky =N+S+E+W)

    addcoin = Button(pycrypto,text="Add coin",bg="orange",fg="black",command=addcoin,font="Lato 14 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    addcoin.grid(row=coin_row+1,column=4,sticky =N+S+E+W)  
     #updatecoin

    port_idu = Entry(pycrypto,borderwidth=2,relief="groove")
    port_idu.grid(row=coin_row+2,column=0,sticky =N+S+E+W)

    symbol_up = Entry(pycrypto,borderwidth=2,relief="groove")
    symbol_up.grid(row=coin_row+2,column=1,sticky =N+S+E+W)

    price_up = Entry(pycrypto,borderwidth=2,relief="groove")
    price_up.grid(row=coin_row+2,column=2,sticky =N+S+E+W)

    amount_up = Entry(pycrypto,borderwidth=2,relief="groove")
    amount_up.grid(row=coin_row+2,column=3,sticky =N+S+E+W) 

    updatecoin = Button(pycrypto,text="Update Coin",bg="orange",fg="black",command=updatecoin,font="Lato 14 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    updatecoin.grid(row=coin_row+2,column=4,sticky =N+S+E+W) 

    #DELETECOIN
    pfid_del = Entry(pycrypto,borderwidth=2,relief="groove")
    pfid_del.grid(row=coin_row+3,column=3,sticky =N+S+E+W) 

    deletecoin = Button(pycrypto,text="Delete Coin",bg="orange",fg="black",command=deletecoin,font="Lato 14 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    deletecoin.grid(row=coin_row+3,column=4,sticky =N+S+E+W) 
  
    total_current = Label(pycrypto,text="${0:.2f}".format(total_cv),bg="white",fg=fontcolor(float("{0:.2f}".format(total_cv))),font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    total_current.grid(row=coin_row,column=5,sticky =N+S+E+W)

    totalcp = Label(pycrypto,text="${0:.2f}".format(total_cp),bg="white",fg=fontcolor(float("{0:.2f}".format(total_cv))),font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    totalcp.grid(row=coin_row,column=4,sticky =N+S+E+W)

    total_plc = Label(pycrypto,text="${0:.2f}".format(total_pl),bg="white",fg=fontcolor(float("{0:.2f}".format(total_pl))),font="Lato 12 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    total_plc.grid(row=coin_row,column=7,sticky =N+S+E+W)

    api =""
    refresh = Button(pycrypto,text="Refresh",bg="orange",fg="black",command=reset,font="Lato 14 bold",padx="4",pady="4",borderwidth=2,relief="groove")
    refresh.grid(row=coin_row+1,column=7,sticky =N+S+E+W)

def app_header():
    pf_id = Label(pycrypto,text="Portfolio ID",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    pf_id.grid(row=0,column=0,sticky =N+S+E+W)

    name = Label(pycrypto,text="Coin Name",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    name.grid(row=0,column=1,sticky =N+S+E+W)

    price = Label(pycrypto,text="Price",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    price.grid(row=0,column=2,sticky =N+S+E+W)

    no_owned= Label(pycrypto,text="Coin owned",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    no_owned.grid(row=0,column=3,sticky =N+S+E+W)

    amount_paid = Label(pycrypto,text="Total Amount Paid",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    amount_paid.grid(row=0,column=4,sticky =N+S+E+W)

    current_value = Label(pycrypto,text="Current Value",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    current_value.grid(row=0,column=5,sticky =N+S+E+W)

    profit_per_c = Label(pycrypto,text="Total P/L per coin",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    profit_per_c.grid(row=0,column=6,sticky =N+S+E+W)

    total_pl = Label(pycrypto,text="Total P/L ",bg="orange",fg="black",font="Lato 14 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    total_pl.grid(row=0,column=7,sticky =N+S+E+W)

app_nav()
app_header()
my_pf()
pycrypto.mainloop()

curobj.close()
con.close()

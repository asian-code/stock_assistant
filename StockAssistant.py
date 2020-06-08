import os
import sys
import requests
import json
import webbrowser
import time
import platform
from datetime import date
from datetime import datetime
from tkinter import filedialog
from tkinter import *


filename="myStocks"
r = '\033[0m'  # reset
bold = '\033[01m'
d = '\033[02m'  # disable
ul = '\033[04m'  # underline
reverse = '\033[07m'
st = '\033[09m'  # strikethrough
invis = '\033[08m'  # invisible
white = '\033[0m'
cwhite = '\33[37m'
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
orange = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'
lgrey = '\033[37m'
grey = '\033[90m'
lred = '\033[91m'
lgreen = '\033[92m'
yellow = '\033[93m'
lblue = '\033[94m'
pink = '\033[95m'
lcyan = '\033[96m'
bgreen = '\33[42m'
blgreen = '\33[102m'
bred = '\33[41m'
blred = '\33[101m'
borange = '\33[43m'
byellow = '\33[33m'
bcyan = '\33[44m'
blcyan = '\33[104m'
br = '\33[108m'
brown = '\33[33m'
bwhite = '\33[107'

url = "https://alpha-vantage.p.rapidapi.com/query"
querystring = {"symbol":"","function":"GLOBAL_QUOTE"}
headers = {'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",'x-rapidapi-key':"fa3f62a263mshdb10554a622214ep10f92ejsn34fca50a787f"}
#to do list 
# windows support (code freeze) pyinstaller -F -i StockAssistant.ico StocksAssistant.py
def logo():
    print('''{2}
        ____  _             _            
       / ___|| |_ ___   ___| | __        
       \___ \| __/ _ \ / __| |/ /        
        ___) | || (_) | (__|   <         
       |____/ \__\___/_\___|_|\_\ {0}   _   
   __ _ ___ ___(_)___| |_ __ _ _ __ | |_ 
  / _` / __/ __| / __| __/ _` | '_ \| __|
 | (_| \__ \__ | \__ | || (_| | | | | |_ 
  \__,_|___|___|_|___/\__\__,_|_| |_|\__|
{1}
 https://github.com/asian-code/stock_assistant/ {0}
            Made by Asian-code                               
'''.format(green,cyan,yellow)+r)

def clearScreen():
    if platform.system()=="Windows":
        os.system("cls")
    else:
        os.system("clear")
        
def SaveToFile(option):
    global filename
    # cache today data and time
    now = datetime.now()
    today = date.today()
    current_date = today.strftime("%m/%d/%Y")
    current_time = now.strftime("%H:%M")
    #add all [gain %] to a sorted list
    ratios=[]
    for i in Entry:
        ratios.append(i[3])
    ratios=sorted(ratios,reverse=True)
    #build results based on order of ratios
    results=[]
    for i in ratios:# i = ratio
        for x in Entry: # x= element
                if i == x[3]:
                    Entry.remove(x)
                    results.append(x)

    # Filename                
    nameInput=input("{2}[*] Enter file name (default = {1}{0}{2}):{1} ".format(filename,green,r))
    # if input is empty
    if nameInput != "":
        filename=nameInput
    try:
        # save to html table
        if option=="1":
            filename+=".html"
            f=open(filename,"w")
            f.write("Created on {0} at {1}".format(current_date,current_time))
            f.write('''<style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:100;border-color:#9ABAD9;margin:0px auto;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#9ABAD9;color:#444;background-color:#EBF5FF;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#9ABAD9;color:#fff;background-color:#409cff;}
    .tg .TopRow{font-size:22px;font-family:"Arial Black", Gadget, sans-serif !important;;border-color:inherit;text-align:center;vertical-align:top;position:sticky;position:-webkit-sticky;top:-1px;will-change:transform}
    .tg .row1{background-color:#D2E4FC;font-size:22px;font-family:Arial, Helvetica, sans-serif !important;;border-color:inherit;text-align:center;vertical-align:top}
    .tg .row2{font-size:22px;font-family:Arial, Helvetica, sans-serif !important;;border-color:inherit;text-align:center;vertical-align:top}
    </style>
    <div align="center"><h3>Best value stocks are on the top of chart</h3></div>
    <table class="tg">
        <tr>
        <th class="TopRow">Stock</th>
        <th class="TopRow">Buy/Sell</th>
        <th class="TopRow">Profit Per Share</th>
        <th class="TopRow">% Gain</th>
        </tr>
    ''')
            c=0 # counter between css :row1, row2
            for i in results:
                f.write("<tr>")
                for x in i:
                    if c % 2==0:
                        f.write('<td class="row2">'+str(x)+'</td>')
                    else:
                        f.write('<td class="row1">'+str(x)+'</td>')
                f.write("<tr>")
                c+=1
            f.write("</table>")

            # save data in html comment for future import

            # save data as json
            data={}
            for i in results:
                data[i[0]]=i[1]
            # write json into file
            f.write("<!--Stock Data ")
            f.write(json.dumps(data))
            f.write("-->")
            f.close()

        # save to text file
        if option =="0":
            filename+=".txt"
            f=open(filename,"w")
            f.write("Created on {} at {}\n".format(current_date,current_time))
            f.write("\nStock\t\t{0:<12}\t\t{1:<6}\t\tGain %\n".format("Buy / Sell","Profit"))
            for i in results:
                f.write("\n{0:<4}\t\t{1:<12}\t\t${2:<6}\t\t{3}%".format(i[0],i[1],i[2],i[3]))
            f.close()
        # tell user the results have been saved
        location=resource_path(filename)
        print(green+"[+] Results have been saved!"+r)
        print(green+"[+] File located at "+cyan+location+r)
        # Auto open the saved file for user to see
        webbrowser.open(location, new=2)
    except:
        print(red,"[!] A problem occured while trying to save to file, please try again"+r)
        report=input("[*] Would you like to report this issue? (y/n): ")
        if report.lower()=="y":
            link="https://github.com/asian-code/stock_assistant/issues/new"
            print(cyan+bold+"[!] Please screenshot the error message and post it on "+green+link+r)
            print("---Error Message--------------------------------")
            raise
            time.sleep(3)
            webbrowser.open(link,new=2)

def Display():
    if len(Entry)>0:
        print("---{0}Saved Stocks{1}--------------------------------------------".format(green,r))   
        print("{0}Name\t\t{2:<12}\t\t{3}\t\tGain %{1}".format(cyan,r,"Buy / Sell","Profit"))
        # loop through each tuple
        # string formatting with field width specifiers for chart
        for i in Entry:
            print("{0:<4}\t\t{1:<12}\t\t{2:<6}\t\t{3}%".format(i[0],i[1],i[2],i[3]))
        print("-----------------------------------------------------------")

def GetStockPriceOFFLINE():
    price=0
    valid=False
    while not valid:
        try:
            print(cyan+"---Getting stock buy price manually-----------------------")
            price=float(input(r+"[*] Current Price of stock: "+green))
            valid=True
        except:
            print(red,"[!] Not a valid price",r)
            valid=False
    return price

def requestFeedback():
    link="https://github.com/asian-code/stock_assistant/issues/new"
    idea=input(r+"\n---{0}Got Feedback/Ideas/Issues? {1}-----------------------------\n Think the tool can be better?\n Would you like to send feedback? (y/n): ".format(cyan,r))
    if idea.lower()=="y":
        print(cyan+bold+link+r)
        time.sleep(2)
        webbrowser.open(link,new=2)

def quit():
    userSelect="0"# default = save to text file
    logo()
    Display()
    if len(Entry)>0:
        save=input("\n\n{0}[*] Would you like to save file?{1} (y/n): ".format(green,r))
        if save.lower()=="y":

            #check valid selected option 
            valid=False
            while not valid:
                clearScreen()
                Display()
                print("\n---{0}Options{1}---------------------------".format(cyan,r))
                print("\n{1} [{0}0{1}] Save as a text file (.txt)\n [{0}1{1}] Save as a html table (.html)\n".format(green,r))
                print("--------------------------------------")
                userSelect=input("[*] Select an option: "+green)
                if userSelect=="0" or userSelect =="1":
                    valid=True

            SaveToFile(userSelect)
            requestFeedback()
            
    else:
        print(green,"[+] Exiting program",r)

def getStockPrice(ticker):
    querystring["symbol"]=ticker
    #print(querystring)
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        test=json.loads(response.text)
        try:
            for i in test.values():
                return round(float(i["05. price"]),2)
        except:
            return False
    else:
        return False

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def getImportLocation():
    root = Tk().withdraw(
        )  # withdraw prevents the tiny window from popping up
    location = filedialog.askopenfilename(initialdir="/~",title="Select file",filetypes=(("html files","*.html"),("all files", "*.*")))
    if location == "":
        print(red + "[!] No file was selected" + r)
        return False
    return location
    
def processHTMLImport(location):
    # get json data from html table
    file=open(location,"r")
    data=file.read()
    file.close()
    if "<!--Stock Data " not in data:
        print(red+"[!] Didnt detect any stock data"+r)
        return KeyboardInterrupt
    data=data.split("<!--Stock Data ")
    data=data[1].split("-->")[0]# json data
    data=json.loads(data)# turns into a dictionary
    # get sell price isolated 
    for i in data.keys():
        data[i]=float(data[i].split("/$")[1])
    return data
    
def CreateEntry(name,buy,sell):
    profit=round(sell-buy,2)
    ratio=round(profit/buy*100,2)
    #save to list ,order of data =(Name,buy/sell,profit,ratio)
    return [name,"${0}/${1}".format(buy,sell),"$"+str(profit),ratio]

try:
    Entry=[]
    while True:
        cprice=0
        oprice=0
        name=""
        logo()
        Display()
        print()
        # quit
        print(" Press '{0}Contorl+c{1}' or '{0}Crtl+c{1}' to quit/save".format(cyan,r))
        print(" Enter '{0}import{1}' to update a html table\n".format(cyan,r))
        name=input(r+"[*] Ticker symbol of stock: "+green).upper()
        name=name.replace(" ","")# get rid of whitespace
        print(r)# resets color
        if name.upper()=="0":
            raise KeyboardInterrupt
        elif name.lower()=="import":
            fileLocation=getImportLocation()
            stocks=processHTMLImport(fileLocation)# returns dic of stocks in (name:)
            #display detected stocks from html table
            clearScreen()
            print(r+"---{0}Detected Imported Stocks{1}------------------------".format(green,r))
            print(cyan+"Name\t\tSell"+r)
            for i in stocks.keys():
                print("{0:<5}\t\t${1}".format(i,stocks[i]))
            print("----------------------------------------------")
            # get info for each stock
            for i in stocks.keys():
                # set name
                name=i
                # get buy price
                cprice=getStockPrice(i)
                if cprice is False:
                    print("{0}[!] Unable to determine stock price for {1}{2}{3}".format(red,green,i,r))
                    cprice= GetStockPriceOFFLINE()
                # set sell price
                oprice=stocks[i]
                
                Entry.append(CreateEntry(name,cprice,oprice))
            quit()
            break

        # Get Current Price
        autoInfo=input("{0}[*] Get the current price of {1}{2}{0} automatically? (y/n): ".format(r,green,name))
        if autoInfo.lower()=="y":
            # get price online through API
            cprice=getStockPrice(name)
            # if cant get stock data
            if cprice==False:
                print(red+"[!] Could not get data for this stock,perhaps misspelled?"+r)
                cprice=GetStockPriceOFFLINE()
            else:
                print(cyan+"---Getting current Stock buy price automatically-----------------------")
                print(green+"[+] Detected price: ",r,cprice)

        else:
            # get current price(offline method)
            cprice=GetStockPriceOFFLINE()
        
        # get sell price
        valid=False
        while not valid:
            try:
                oprice=float(input(r+"[*] Sell Price of stock: "+green))
                valid=True
            except:
                print(red,"[!] Not a valid price",r)
                valid=False
        
        Entry.append(CreateEntry(name,cprice,oprice))
        print(r)
        clearScreen()
except KeyboardInterrupt:
    print(r)
    clearScreen()
    quit()

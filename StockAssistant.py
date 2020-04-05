import os
import requests
import json

cprice=0
oprice=0
name=""
Entry=[]
filename="myStocks.txt"
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
# sorting method
# export to html file (table)
# windows support (code freeze)
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

def SaveToFile():
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

    # save to text file
    f=open(filename,"w")
    f.write("\nName\t\tBuy/Sell\t\t\tProfit\t\tGain %\n")
    for i in results:
        f.write("{0}\t\t{1}\t\t${2}\t\t{3}%".format(i[0],i[1],i[2],i[3]))
    f.close()

def Display():
    if len(Entry)>0:
        print("---{0}Saved Stocks{1}--------------------------------------------".format(green,r))   
        print(cyan,"Name\t\tBuy/Sell\t\t\tProfit\t\tGain %",r)
        # loop through each tuple
        for i in Entry:
            print("{0}\t\t{1}\t\t${2}\t\t{3}%".format(i[0],i[1],i[2],i[3]))
        print("-----------------------------------------------------------")

def GetStockPriceOFFLINE():
    global cprice
    valid=False
    while not valid:
        try:
            print(cyan+"---Getting stock buy price manually-----------------------")
            cprice=float(input(r+"[*] Current Price of stock: "+green))
            valid=True
        except:
            print(red,"[!] Not a valid price",r)
            valid=False

def quit():
    global filename
    if len(Entry)>0:
        save=input("\n\n{0}[*] Would you like to save file?{1} (y/n): ".format(green,r))
        if save=="y":
            nameInput=input("[*]Enter file name (default name = {0}): ".format(filename))
            #use default name if input is empty
            if nameInput != "":
                filename=nameInput+".txt"
            # support for md files coming soon----------------------------------
                
            print(bold+"[+] Saving to file: {0}{2}{1}".format(green,r,filename))
            SaveToFile()
            print(green,"[+] Saved File, exiting program",r)
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

try:
    while True:
        logo()
        Display()
        print()
        # quit
        print(" Press '{0}Contorl+c{1}' or '{0}Crtl+c{1}' to quit/save\n".format(cyan,r))
        name=input(r+"[*] Ticker symbol of stock: "+green).upper()
        if name.upper()=="0":
            raise KeyboardInterrupt

        # Get Current Price
        autoInfo=input("{0}[*] Get the current price of {1}{2}{0} automatically? (y/n): ".format(r,green,name))
        if autoInfo.lower()=="y":
            # get price online through API
            cprice=getStockPrice(name)
            # if cant get stock data
            if cprice==False:
                print("[!] Could not get data for this stock")
                GetStockPriceOFFLINE()
            else:
                print(cyan+"---Getting current Stock buy price automatically-----------------------")
                print(green+"[+] Detected price: ",r,cprice)

        else:
            # get current price(offline method)
            GetStockPriceOFFLINE()
        
        
        # get sell price
        valid=False
        while not valid:
            try:
                oprice=float(input(r+"[*] Sell Price of stock: "+green))
                valid=True
            except:
                print(red,"[!] Not a valid price",r)
                valid=False
        
        profit=round(oprice-cprice,2)
        ratio=round(profit/cprice*100,2)
        #save to list order of (Name,buy/sell,profit,ratio)
        Entry.append([name,"${0}/${1}".format(cprice,oprice),profit,ratio])
        #"{0}\t\t${3}/${4}\t\t${1}\t\t{2}".format(name,profit,ratio,cprice,oprice)
        #print(Entry)
        print(r)
        os.system("clear")
except KeyboardInterrupt:
    print(r)
    os.system("clear")
    logo()
    Display()
    quit()

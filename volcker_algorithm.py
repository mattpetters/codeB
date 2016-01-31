import socket
import sys, time, math, os

username = "Volcker"
password = "bernankescrisis"
database = {}
timeHeldSec = {}


def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429

    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        output = ""
        while rline:
            output = rline.strip()
            rline = sfile.readline()

            return output

    finally:
        sock.close()

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429

    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def main():
    print runCommand("CLOSE_CONNECTION")
    securities = getSecurities()

    while(True):
        print "Restart!"
        print runCommand("MY_SECURITIES")
        for sec in securities:
            database = createSecurityDict()
            trade(sec, database)
            # print runCommand("MY_SECURITIES")
            print "Total cash: ", getMyCash()

    
def getSecurities():
    string = runCommand("SECURITIES")
    output = string.split()

    securitiesList = []
    for i in range(1, len(output), 4):
        securitiesList.append(output[i])
    print securitiesList
    return securitiesList

#     securities = ["AAPL", "GM", "C", "CMG", "DELL", "DIS", "F", "JPY", "XOM", "IBM"]
#     

# def buy(security):
# 

# def sell(security):

# def getVolitility(security):


# def getPrice(security):


# def getDivRatio(security):

# def getNetWorth(security):

# def getSecurities(responseString):

def runCommand(call):
    return run(username, password, call)


# Returns dictionary of securities with data
# To index into specific data use:
# securities['TICKER']['DATAKEY']
# Datakeys are as follows:
# netWorth, divRatio, volatility, bidPrice, askPrice, bidShares, askShares
def createSecurityDict():
    securities = {}
    output = runCommand("SECURITIES")
    splitString = output.split()


    for i in range(1, len(splitString),4):
        securities[splitString[i]] = {'netWorth':splitString[i+1],
        'divRatio':splitString[i+2],
        'volatility':splitString[i+3]}


    for security in securities:
        bidString = runCommand("ORDERS " + security).split()
        securities[security]["bidPrice"] = bidString[3]
        securities[security]["askPrice"] = bidString[7]
        securities[security]["bidShares"] = bidString[4]
        securities[security]["askShares"] = bidString[8]

    return securities

def buy(security, price, shares):
    order = "BID " + security.upper() + " " + str(price) + " " + str(int(shares))
    print "BOUGHT %s: %s" % (security, runCommand(order))

def sell(security, price, shares):
    order = "ASK " + security.upper() + " " + str(price) + " " + str(int(shares))
    print "SOLD %s: %s" % (security, runCommand(order))


def getMyCash():
    cashRaw = runCommand("MY_CASH")
    output = cashRaw.split()
    return output[1]
# print getMyCash()

def getMarketValue(ticker, database):
    bidPrice = float(database[ticker]["bidPrice"])
    numBids = float(database[ticker]["bidShares"])

    askPrice = float(database[ticker]["askPrice"])
    numAsks = float(database[ticker]["askShares"])

    return float((bidPrice * numBids) + (askPrice * numAsks)) / float(numAsks + numBids)
# print getMarketValue("NFLX")
# print runCommand("ORDERS NFLX")

def numSharesSec(ticker):
    secs = runCommand("MY_SECURITIES")
    output = secs.split()
    val = output[output.index(ticker) + 1]
    return val


def isSelling(ticker):
    blah = "ORDERS" + " " + str(ticker)
    string = runCommand(blah)
    # print string
    output = string.split()

    if "ASK" in output:
        return True
    else:
        return False

def isBuying(ticker):
    blah = "ORDERS" + " " + str(ticker)
    string = runCommand(blah)
    # print string
    output = string.split()

    if "BID" in output:
        return True
    else:
        return False


def trade(security, db):
    print "=======Determining trade for: %s=================" % str(security)
    myCash = getMyCash();
    numShares = numSharesSec(security)
    # for each security, check:
    # BUY
    # is market value (vol*avg(bid+ask)) < net worth
    marketVal = float(getMarketValue(security, db))
    bidPrice = float(db[security]["bidPrice"])
    askPrice = float(db[security]["askPrice"])

    # print marketVal, bidPrice, askPrice

    # if market val is less than what people want to buy at, sell everything
    if (marketVal < bidPrice):

        print "in sell"
        # determine what percent of portfolio allocated to this share by making it a ratio of networth/market value difference
        # percentAllocation = (((security.networth - marketValue(security))/security.netWorth))*80)/100
        # numSharesBuy = floor((myCash*0.1)/security.pricePerShare);
        # runCommand(buy(security, PRICE FROM..., NUM SHARES FROM....))
        y = float(numSharesSec(security))
        if y > 0:         
            print "numshares to sell: ", y
            if isSelling(security):
                sell(security, float(bidPrice) , y)
            else:
                print runCommand("CLEAR_ASK")
    # buy
    # print buy(security, askPrice, 1)
    if (marketVal >= float(askPrice) or (marketVal - askPrice) < 1):
        print "in buy"
        x = ((bidPrice - marketVal)/ bidPrice * float(getMyCash()))
        
        if x > 0:
            numSharesToBuy = math.floor(x/float(askPrice))
        else:
            return
        if numSharesToBuy > 0:
            print "numshares to buy: ", numSharesToBuy
            if isBuying(security):
                buy(security, float(askPrice), numSharesToBuy)
            else:
                print runCommand("CLEAR_BID")
    print sell(security, bidPrice - 0.5, 2)

if __name__ == "__main__": main()
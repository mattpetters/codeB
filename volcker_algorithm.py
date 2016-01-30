import socket
import sys, time

username = "Volcker"
password = "bernankescrisis"
database = {}
securitiesOwned = {}

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

# while True:
#     time.sleep(1)
#     database = createSecurityDict()

# def trade(security):
    # marketCap = run()
    # netWorth = run(security +)



# def getMarketCap(ticker):




def buy(security, price, shares):
    order = "BID " + security.upper() + " " + str(price) + " " + str(float(shares))
    print runCommand(order)

def sell(security, price, shares):
    order = "ASK " + security.upper() + " " + str(price) + " " + str(float(shares))
    print runCommand(order)


def getMyCash():
    cashRaw = runCommand("MY_CASH")
    output = cashRaw.split()
    return output[1]
# print getMyCash()

def getMarketValue(ticker):
    bidPrice = float(database[ticker]["bidPrice"])
    numBids = float(database[ticker]["bidShares"])

    askPrice = float(database[ticker]["askPrice"])
    numAsks = float(database[ticker]["askPrice"])

    return float((bidPrice * numBids) + (askPrice * numAsks)) / float(numAsks + numBids)

def buyStock():
    securities = createSecurityDict()
    number = 10
    for security in securities:
        print security
        print "BID " + security + " " + str(securities[security]['askPrice']) + " " + str(number)
        #securitiesOwned[security] = securitiesOwned[security] + number
        print runCommand("BID " + security + " " + str(securities[security]['askPrice']) + " " + str(number))

def sellStock():
    securities = createSecurityDict()
    number = 10
    for security in securities:
        print security
        print "ASK " + security + " " + str(securities[security]['bidPrice']) +  " " + str(number)
        #securitiesOwned[security] = securitiesOwned[security] + number
        print runCommand("ASK " + security + " " + str(securities[security]['bidPrice']) +  " " + str(number))


def ourSecurities():
    return "We own :".join(securitiesOwned)

# def trade(security, db):
#     myCash = getMyCash();
#     numShares = numSharesThisSecurity(security)
#     # for each security, check:
#     # BUY
#     # is market value (vol*avg(bid+ask)) < net worth
#     if (marketValue(security) < db[security]["netWorth"])
#         # determine what percent of portfolio allocated to this share by making it a ratio of networth/market value difference
#         # percentAllocation = (((security.networth - marketValue(security))/security.netWorth))*80)/100
#         numSharesBuy = floor((myCash*0.1)/security.pricePerShare);
#         runCommand(buy(security, PRICE FROM..., NUM SHARES FROM....))
#     # SELL
#     else {
#         sell(security, ,numShares)
#     }
#     marketValue = (security.bid + secuirty.ask) / security.volume
while True:
    ourSecurities()
    buyStock()
    time.sleep(3)
    sellStock()

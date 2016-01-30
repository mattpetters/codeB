import socket
import sys, time

username = "Volcker"
password = "bernankescrisis"
database = {}
    
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
            # getOutput(rline.strip())
            # print rline.strip()
            #output.append(rline.strip())
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


# def main():
#     securities = getSecurities()

#     for security in securities:
#         database = createSecurityDict()
#         trade(security, database)


def handleOperations():
 run(username, password, "SECURITIES")
    

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


# def getSecurities():
#     securities = []
#     output = runCommand("SECURITIES")
#     print "output: " , output

#     for i in range(1,len(output), 4):
#          securities.append(output[i])
#     # print securities
#     # return securities
# getSecurities()


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
        print runCommand("ORDERS " + security)
        bidString = runCommand("ORDERS " + security).split()
        securities[security]["bidPrice"] = bidString[3]
        securities[security]["askPrice"] = bidString[7]
        securities[security]["bidShares"] = bidString[4]
        securities[security]["askShares"] = bidString[8]


    # print securities
    return securities

# while True:
#     time.sleep(1)
#     database = createSecurityDict()

# createSecurityDict()

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
    database = createSecurityDict()
    bidPrice = float(database[ticker]["bidPrice"])
    numBids = float(database[ticker]["bidShares"])

    askPrice = float(database[ticker]["askPrice"])
    numAsks = float(database[ticker]["askPrice"])

    return float((bidPrice * numBids) + (askPrice * numAsks)) 
    # / float(numAsks + numBids)




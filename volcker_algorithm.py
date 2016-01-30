import socket
import sys

username = "Volcker"
password = "bernankescrisis"
    
def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        output = []
        while rline:
            # getOutput(rline.strip())
            # print rline.strip()
            output.append(rline.strip())
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
    return run("Volcker", "bernankescrisis", call)


def getSecurities():
    securities = []
    output = runCommand("SECURITIES")
    print "output: " , output

    for i in range(1,len(output), 4):
         securities.append(output[i])
    # print securities
    # return securities
getSecurities()

def createSecurityDict(responseString):
    print responseString
    securities = {}
    splitString = responseString.split()
    
    for i in range(1, len(splitString),4):
        securities[splitString[i]] = {'netWorth':splitString[i+1],
        'divRatio':splitString[i+2],
        'volatility':splitString[i+3]}

    print securities
    return securities

handleOperations()

# def trade(security):
    # marketCap = run()
    # netWorth = run(security +)



# def getMarketCap(ticker):
    



def buy(security, price, shares):
    order = "BID " + security.upper() + " " + str(price) + " " + str(float(shares))
    run(username, password, order)
def sell(security, price, shares):
    order = "ASK " + security.upper() + " " + str(price) + " " + str(float(shares))
    run(username, password, order)







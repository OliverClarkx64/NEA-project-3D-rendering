import numpy as np
###calculator###
##functions of arithmetic operations
def add(executable):
    return float(executable[0]) + float(executable[1])

def multiply(executable):
    return float(executable[0]) * float(executable[1])

def divide(executable):
    try:
        return float(executable[0])/float(executable[1])
    except:
        return 0

def subtract(executable):
    return float(executable[0]) - float(executable[1])

def power(executable):
    return float(executable[0])**float(executable[1])

        
##hashmap = {"+":add,
##           "-":subtract,
##           "*":multiply,
##           "/":divide,
##           "**":power}

##splitter algorithm        
def priority(data):
    ##gets the range for the brackets
##    if "(" in data:
##        brackets = [[],[]] 
##        for i in range(len(data)):
##            if data[i] == "(":
##                brackets[0].append(i)
##            elif data[i] == ")":
##                brackets[1].append(i)
##    ##gets whats inside of the outer most brackets
##        a = priority(data[brackets[0][0] + 1:brackets[1][-1]])
##        ##parses the bracket string throught the function again
##        return priority(data[:brackets[0][0]] + str(a) + "".join([str(elem) for elem in data[brackets[1][-1]+1:]]))                              ##as long as the brackets come first it works
##    ##checks the least prioritised operation  "-"     
##    ##checks for addition
    if "(" in data:
        data = data.split("(",1)
        data_l = data[0]#priority(data[0])
        data_r = str(priority(data[1]))
        return priority(data_l + data_r)
    elif ")" in data:
        data = data.split(")",1)
        data_l = str(priority(data[0]))
        data_r = data[1]#priority(data[1])
        return priority(data_l + data_r)
    
    elif "+" in data:
        try:
            data = float(data)
            return data
        except:
            data = data.split("+",1)
            data_l = priority(data[0])
            data_r = priority(data[1])
            return add([data_l,data_r])
    elif "-" in data:
        try:
            data = float(data)
            return data
        except:
            data = data.split("-",1)
            data_l = priority(data[0])
            data_r = priority(data[1])
            return subtract([data_l,data_r])
    ##checks for division
    elif "/" in data:
        data = data.split("/",1)
        data_l = priority(data[0])
        data_r = priority(data[1])
        return divide([data_l,data_r])
    ##checks for multiplication
    elif "*" in data:
        data = data.split("*",1)
        data_l = priority(data[0])
        data_r = priority(data[1])
        return multiply([data_l,data_r])
    ##checks for powers
    elif "^" in data:
        data = data.split("^",1) #splits everything at "^"
        data_l = priority(data[0]) #takes everything left of "^"
        data_r = priority(data[1]) #takes everything right of "^"
        return power([data_l,data_r]) #applies the power function to them
    ##checks for sin
    elif "sin" in data:
        data = data.split("sin",1) #splits everything as sin
        data_r = priority(data[1])    #recurses everything right os sin                                          ##because sin only takes everything right of the sin
        return np.sin(float(data_r))   #returns the operaton of cos
    ##checks for cos
    elif "cos" in data:
        data = data.split("cos",1) #splits everything at cos
        data_r = priority(data[1])  #recurses everything right of cos                            ##because cos only takes everything right of the sin
        return np.cos(float(data_r)) #retrns the operation of cos

    ##checks for tan
    elif "tan" in data:
        data = data.split("tan",1)
        data_r = priority(data[1])                              ##because tan only takes everything right of the sin
        return np.tan(float(data_r))
    ##checks for log
    elif "log" in data: ##log base e or ln
        data = data.split("log",1)
        data_r = priority(data[1])                              ##because log only takes everything right of the sin
        return np.log(float(data_r))
    
    else:
        return data
##while (a := input(":")) != "stop":
##    print(priority(a))
##
##while a:= True == True:
##    print(priority((b := input(": "))))
##    if b == "stop":
##        a = False
##data_l = priority(data[0])  these functions are what make the recursion - they take the simple operations and apply the 
##data_r = priority(data[1])        same algorithm to everything left and right of the operation. This is how i make the
##                                    priority as the most prioritised operation to a digit will actually be executed first
##                                    even if the search function finds the least prioritised operation first - it splits it and finds
##                                    the more prioritised operations at the bottom of the recursion and closest to the numbers-
##                                    even if this links to a bracket-the bracket works the same way by executing everything inside
##                                    of it, appending that back to the equation and then running that through the procedure again-

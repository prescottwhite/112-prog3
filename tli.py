#! /usr/bin/env python3
import fileinput
import sys


# used to store a parsed TL expressions which are
# constant numbers, constant strings, variable names, and binary expressions
# operators: num, str, var, +, -, *, /, ==, <, >, <=, >=, !=
class Expr:
    def __init__(self, op1, operator, op2=None):
        self.op1 = op1
        self.operator = operator
        self.op2 = op2

    def __str__(self):
        if self.op2 == None:
            return self.operator + " " + self.op1
        else:
            return self.op1 + " " + self.operator + " " +  self.op2

    # evaluate this expression given the environment of the symTable
    def eval(self, symTable):
        if self.operator == "var":
            return symTable[op1]
        else:
            return 0


# used to store a parsed TL statement
class Stmt:
    def __init__(self, lineNum, keyword, exprs):
        self.lineNum = lineNum
        self.keyword = keyword
        self.exprs = exprs

    def __str__(self):
        others = ""
        for exp in self.exprs:
            others = others + " " + str(exp)
        return self.keyword + others

    # perform/execute this statement given the environment of the symTable
    def perform(self, symTable):
        if self.keyword == "let":
            symTable[self.exprs[0]] = self.exprs[1].eval(symTable)
        if self.keyword == "if":
            if (self.exprs[0].eval(symTable)) == 0:
                # go to next statement
            else:
                # goto line number that label indicates

# read 1st argument when calling script
fileName = sys.argv[1]

# open file with given filename
file = open(fileName, "r")

# line number, symbol and label tables, statement list
lineNum = 0
symTable = {}
labelTable = {}
stmtList = []

for x in file:
    labelIndex = 0
    lineNum += 1
    lineParsed = x.split()
    numTokens = len(lineParsed)
    exprList = []
	
    # if line is not empty
    if (numTokens != 0):

        # if there is a label
        if lineParsed[0].endswith(':'):
            # store label without colon
            labelTable[lineParsed[0][:-1]] = lineNum
            # rest of statement will start one index over
            labelIndex = 1
    
	    exprIndex = labelIndex + 1
        keyword = lineParsed[labelIndex]

        if keyword == "let":
            lineParsed.remove("=")
            # add variable name
            exprList.append(Expr(lineParsed[exprIndex], "var"))
            # if form is 'let variable = value' where '=' is removed and value is either float or string
            if (numTokens - labelIndex) == 3:
                if is_number(lineParsed[exprIndex + 1]):
                    exprList.append(Expr(lineParsed[exprIndex + 1], "num"))
                else:
                    exprList.append(Expr(lineParsed[exprIndex + 1], "str"))
            # if form is 'let variable = value operator value' where '=' is removed and value is either float or variable
            elif (numTokens - labelIndex) == 5:
                exprList.append(Expr(lineParsed[exprIndex + 1], lineParsed[exprIndex + 2], lineParsed[exprIndex + 3]))
            stmtList.append(Stmt(lineNum, keyword, exprList))

        elif keyword == "if":
            lineParsed.remove("goto")
            if (numTokens - labelIndex) == 3:
                if is_number(lineParsed[exprIndex + 1]):
                    exprList.append(Expr(lineParsed[exprIndex + 1], "num"))
                else:
                    exprList.append(Expr(lineParsed[exprIndex + 1], "str"))
            elif (numTokens - labelIndex) == 5:
                exprList.append(Expr(lineParsed[exprIndex], lineParsed[exprIndex + 1], lineParsed[exprIndex + 2]))
            # add label to end of statement, this is the label to goto if expression is true
            exprList.append(Expr(lineParsed[-1], "str"))
            stmtList.append(Stmt(lineNum, keyword, exprList))

        elif keyword == "print":
        
        elif keyword == "input":

# found on StackOverflow
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?rq=1
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# for x in labelTable:
    # print(str(labelTable[x]))
# for x in stmtList:
    # print(str(x))
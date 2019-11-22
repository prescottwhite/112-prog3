#! /usr/bin/env python3
import fileinput
import sys


# used to store a parsed TL expressions which are
# constant numbers, constant strings, variable names, and binary expressions
# operators: num, str, var, +, -, *, /, ==, <, >, <=, >=, !=
class Expr:
    legalOps = ["num", "str", "var", "+", "-", "*", "/", "==", "<", ">", "<=", ">=", "!="]
    def __init__(self, lineNum, op1, operator, op2=None):
        self.op1 = op1
        self.operator = operator
        if not(self.operator in Expr.legalOps):
            syntaxError(lineNum)
        self.op2 = op2

    def __str__(self):
        if self.op2 == None:
            # return self.operator + " " + self.op1
            return self.op1
        else:
            return self.op1 + " " + self.operator + " " +  self.op2

    # evaluate this expression given the environment of the symTable
    def eval(self, lineNum, symTable, labelTable):
        if (self.operator == "num"):
            return float(self.op1)
        elif (self.operator == "str"):
            return str(self.op1)
        elif self.operator == "var":
            try:
                varVal = float(symTable[self.op1])
                return varVal
            except KeyError:
                varError(self.op1, lineNum)

        # if variable is being used in expression
        if not(isNumber(self.op1)):
            try:
                x = float(symTable[self.op1])
            except KeyError:
                varError(self.op1, lineNum)
        else:
            x = float(self.op1)
        if not(isNumber(self.op2)):
            try:
                y = float(symTable[self.op2])
            except KeyError:
                varError(self.op2, lineNum)
        else:
            y = float(self.op2)
        
        if self.operator == "+":
            return (x + y)
        elif self.operator == "-":
            return (x - y)
        elif self.operator == "*":
            return (x * y)
        elif self.operator == "/":
            return (x / y)
        elif self.operator == "==":
            if (x == y):
                return 1
            else:
                return 0
        elif self.operator == "<":
            if (x < y):
                return 1
            else:
                return 0
        elif self.operator == ">":
            if (x > y):
                return 1
            else:
                return 0
        elif self.operator == "<=":
            if (x <= y):
                return 1
            else:
                return 0
        elif self.operator == ">=":
            if (x >= y):
                return 1
            else:
                return 0
        elif self.operator == "!=":
            if (x != y):
                return 1
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
    def perform(self, symTable, labelTable):
        if self.keyword == "let":
            symTable[str(self.exprs[0])] = self.exprs[1].eval(self.lineNum, symTable, labelTable)
            return self.lineNum + 1

        elif self.keyword == "if":
            if (self.exprs[0].eval(self.lineNum, symTable, labelTable)) == 0:
                return self.lineNum + 1
            else:
                try:
                    labelNum = labelTable[str(self.exprs[-1])]
                    return labelNum
                except KeyError:
                    gotoError(str(self.exprs[-1]), self.lineNum)

        elif self.keyword == "print":
            strBuilder = ""
            for x in self.exprs:
                strBuilder = strBuilder + str(x.eval(self.lineNum, symTable, labelTable)) + " "
            print(strBuilder)
            return self.lineNum + 1

        elif self.keyword == "input":
            symTable[str(self.exprs[0])] = input()
            return self.lineNum + 1

def parseFile(file, labelTable, stmtList):
    lineNum = 0
    for line in file:
        lineNum += 1
        lineParsed = line.split()
        exprList = []
        
        # if line is not empty
        if (len(lineParsed) != 0):
        
            # if there is a label
            if lineParsed[0].endswith(':'):
                # store label without colon
                labelTable[str(lineParsed[0][:-1])] = lineNum
                lineParsed = lineParsed[1:]
        
            keyword = lineParsed[0]
        
            if keyword == "let":
                lineParsed.remove("let")
                lineParsed.remove("=")
                numTokens = len(lineParsed)
                # add variable name
                exprList.append(Expr(lineNum, lineParsed[0], "var"))
                # if form is 'let variable = value' where value is either float or string
                if (numTokens) == 2:
                    if isNumber(lineParsed[1]):
                        exprList.append(Expr(lineNum, lineParsed[1], "num"))
                    else:
                        exprList.append(Expr(lineNum, lineParsed[1], "var"))
                # if form is 'let variable = value operator value' where '=' is removed and value is either float or variable
                elif (numTokens) == 4:
                    exprList.append(Expr(lineNum, lineParsed[1], lineParsed[2], lineParsed[3]))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "if":
                lineParsed.remove("if")
                lineParsed.remove("goto")
                numTokens = len(lineParsed)
                if (numTokens) == 2:
                    if isNumber(lineParsed[0]):
                        exprList.append(Expr(lineNum, lineParsed[0], "num"))
                    else:
                        exprList.append(Expr(lineNum, lineParsed[0], "var"))
                elif (numTokens) == 4:
                    exprList.append(Expr(lineNum, lineParsed[0], lineParsed[1], lineParsed[2]))
                # add label to end of statement, this is the label to goto if expression is true
                exprList.append(Expr(lineNum, lineParsed[-1], "str"))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "print":
                line = " ".join(lineParsed)
                # remove print
                line = line[5:]
                # split on comma
                lineParsed = line.split(',')
                for x in lineParsed:
                    x = x.strip()
                    if x.startswith('"') and x.endswith('"'):
                        exprList.append(Expr(lineNum, x[1:-1], "str"))
                    else:
                        x = x.split()
                        if len(x) == 1:
                            if isNumber(x[0]):
                                exprList.append(Expr(lineNum, x[0], "num"))
                            else:
                                exprList.append(Expr(lineNum, x[0], "var"))
                        else:
                            exprList.append(Expr(lineNum, x[0], x[1], x[2]))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "input":
                lineParsed.remove("input")
                exprList.append(Expr(lineNum, lineParsed[0], "var"))
                stmtList.append(Stmt(lineNum, keyword, exprList))

            else:
                syntaxError(lineNum)


# found on StackOverflow
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?rq=1
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# error methods
def syntaxError(lineNum):
    print("Syntax error on line " + str(lineNum) + ".")
    sys.exit()

def gotoError(label, lineNum):
    print("Illegal goto " + str(label) + " at line " + str(lineNum) + ".")
    sys.exit()

def varError(varName, lineNum):
    print("Undefined variable " + str(varName) + " at line " + str(lineNum) + ".")
    sys.exit()


def executeStmts(symTable, labelTable, stmtList):
    index = 1
    while (index <= len(stmtList)):
        index = stmtList[index - 1].perform(symTable, labelTable)
    # for x in stmtList[(lineNum - 1):(len(stmtList))]:
        # x.perform(symTable, labelTable, stmtList)
    
def main():
    # read 1st argument when calling script
    fileName = sys.argv[1]
    
    # open file with given filename
    file = open(fileName, "r")
    
    # line number, symbol and label tables, statement list
    lineNum = 1
    symTable = {}
    labelTable = {}
    stmtList = []

    parseFile(file, labelTable, stmtList)
    executeStmts(symTable, labelTable, stmtList)

main()
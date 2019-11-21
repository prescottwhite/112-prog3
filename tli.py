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
            # return self.operator + " " + self.op1
            return self.op1
        else:
            return self.op1 + " " + self.operator + " " +  self.op2

    # evaluate this expression given the environment of the symTable
    def eval(self, symTable, labelTable):
        if (self.operator == "num") or (self.operator == "str"):
            return self.op1
        if self.operator == "var":
            return symTable[self.op1]
        if self.operator == "+":
            return (float(self.op1) + float(self.op2))
        if self.operator == "-":
            return (float(self.op1) - float(self.op2))
        if self.operator == "*":
            return (float(self.op1) * float(self.op2))
        if self.operator == "/":
            return (float(self.op1) / float(self.op2))
        if self.operator == "==":
            if (self.op1 == self.op2):
                return 1
            else:
                return 0
        if self.operator == "<":
            if (self.op1 < self.op2):
                return 1
            else:
                return 0
        if self.operator == ">":
            if (self.op1 > self.op2):
                return 1
            else:
                return 0
        if self.operator == "<=":
            if (self.op1 <= self.op2):
                return 1
            else:
                return 0
        if self.operator == ">=":
            if (self.op1 >= self.op2):
                return 1
            else:
                return 0
        if self.operator == "!=":
            if (self.op1 != self.op2):
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
            symTable[str(self.exprs[0])] = self.exprs[1].eval(symTable, labelTable)

        if self.keyword == "if":
            if (self.exprs[0].eval(symTable, labelTable)) == 0:
                executeStmts(lineNum + 1, symTable, labelTable, stmtList)
            else:
                executeStmts(labelTable[self.exprs[-1]], symTable, labelTable, stmtList)

        if self.keyword == "print":
            for x in self.exprs:
                print(x.eval(symTable, labelTable))

def parseFile(file, labelTable, stmtList):
    lineNum = 0
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
                if (numTokens - labelIndex) == 4:
                    if isNumber(lineParsed[exprIndex + 1]):
                        exprList.append(Expr(lineParsed[exprIndex + 1], "num"))
                    else:
                        exprList.append(Expr(lineParsed[exprIndex + 1], "str"))
                # if form is 'let variable = value operator value' where '=' is removed and value is either float or variable
                elif (numTokens - labelIndex) == 6:
                    exprList.append(Expr(lineParsed[exprIndex + 1], lineParsed[exprIndex + 2], lineParsed[exprIndex + 3]))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "if":
                lineParsed.remove("goto")
                if (numTokens - labelIndex) == 4:
                    if isNumber(lineParsed[exprIndex]):
                        exprList.append(Expr(lineParsed[exprIndex], "num"))
                    else:
                        exprList.append(Expr(lineParsed[exprIndex], "str"))
                elif (numTokens - labelIndex) == 6:
                    exprList.append(Expr(lineParsed[exprIndex], lineParsed[exprIndex + 1], lineParsed[exprIndex + 2]))
                # add label to end of statement, this is the label to goto if expression is true
                exprList.append(Expr(lineParsed[-1], "str"))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "print":
                if (len(lineParsed)) == 2:
                    if isNumber(lineParsed[exprIndex]):
                        exprList.append(Expr(lineParsed[exprIndex], "num"))
                    else:
                        exprList.append(Expr(lineParsed[exprIndex], "var"))
                    stmtList.append(Stmt(lineNum, keyword, exprList))
                    
            # elif keyword == "input":
                # # input logic

            # else:


# found on StackOverflow
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?rq=1
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def executeStmts(lineNum, symTable, labelTable, stmtList):
    for x in stmtList:
        x.perform(symTable, labelTable)
    
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
    executeStmts(lineNum, symTable, labelTable, stmtList)

main()
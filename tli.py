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
        elif self.operator == "var":
            return symTable[self.op1]
        elif self.operator == "+":
            return (float(self.op1) + float(self.op2))
        elif self.operator == "-":
            return (float(self.op1) - float(self.op2))
        elif self.operator == "*":
            return (float(self.op1) * float(self.op2))
        elif self.operator == "/":
            return (float(self.op1) / float(self.op2))
        elif self.operator == "==":
            if (self.op1 == self.op2):
                return 1
            else:
                return 0
        elif self.operator == "<":
            if (self.op1 < self.op2):
                return 1
            else:
                return 0
        elif self.operator == ">":
            if (self.op1 > self.op2):
                return 1
            else:
                return 0
        elif self.operator == "<=":
            if (self.op1 <= self.op2):
                return 1
            else:
                return 0
        elif self.operator == ">=":
            if (self.op1 >= self.op2):
                return 1
            else:
                return 0
        elif self.operator == "!=":
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
    def perform(self, symTable, labelTable, stmtList):
        if self.keyword == "let":
            symTable[str(self.exprs[0])] = self.exprs[1].eval(symTable, labelTable)

        if self.keyword == "if":
            if (self.exprs[0].eval(symTable, labelTable)) == 0:
                executeStmts(self.lineNum + 1, symTable, labelTable, stmtList)
            else:
                executeStmts(labelTable[str(self.exprs[-1])], symTable, labelTable, stmtList)

        if self.keyword == "print":
            for x in self.exprs:
                print(x.eval(symTable, labelTable))

        if self.keyword == "input":
            symTable[str(self.exprs[0])] = input()

def parseFile(file, labelTable, stmtList):
    lineNum = 0
    for x in file:
        labelOffset = 0
        lineNum += 1
        lineParsed = x.split()
        exprList = []
        
        # if line is not empty
        if (len(lineParsed) != 0):
        
            # if there is a label
            if lineParsed[0].endswith(':'):
                # store label without colon
                labelTable[str(lineParsed[0][:-1])] = lineNum
                # lineParsed = lineParsed[1:]
                # rest of statement will start one index over
                labelOffset = 1
        
            keyword = lineParsed[labelOffset]
        
            if keyword == "let":
                lineParsed.remove("let")
                lineParsed.remove("=")
                numTokens = len(lineParsed)
                # add variable name
                exprList.append(Expr(lineParsed[labelOffset], "var"))
                # if form is 'let variable = value' where value is either float or string
                if (numTokens - labelOffset) == 2:
                    if isNumber(lineParsed[labelOffset + 1]):
                        exprList.append(Expr(lineParsed[labelOffset + 1], "num"))
                    else:
                        exprList.append(Expr(lineParsed[labelOffset + 1], "str"))
                # if form is 'let variable = value operator value' where '=' is removed and value is either float or variable
                elif (numTokens - labelOffset) == 4:
                    exprList.append(Expr(lineParsed[labelOffset + 1], lineParsed[labelOffset + 2], lineParsed[labelOffset + 3]))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "if":
                lineParsed.remove("if")
                lineParsed.remove("goto")
                numTokens = len(lineParsed)
                if (numTokens - labelOffset) == 2:
                    if isNumber(lineParsed[labelOffset]):
                        exprList.append(Expr(lineParsed[labelOffset], "num"))
                    else:
                        exprList.append(Expr(lineParsed[labelOffset], "var"))
                elif (numTokens - labelOffset) == 4:
                    exprList.append(Expr(lineParsed[labelOffset], lineParsed[labelOffset + 1], lineParsed[labelOffset + 2]))
                # add label to end of statement, this is the label to goto if expression is true
                exprList.append(Expr(lineParsed[-1], "str"))
                stmtList.append(Stmt(lineNum, keyword, exprList))
        
            elif keyword == "print":
                lineParsed.remove("print")
                for x in lineParsed:
                    if x.endswith(','):
                        # remove comma from expression
                        x = x[:-1]
                    if (x.startswith('"')) and (x.endswith('"')):
                        exprList.append(Expr(x, "str"))
                    elif isNumber(x):
                        exprList.append(Expr(x, "num"))
                    else:
                        exprList.append(Expr(x, "var"))
                stmtList.append(Stmt(lineNum, keyword, exprList))
                                        
            elif keyword == "input":
                lineParsed.remove("input")
                exprList.append(Expr(lineParsed[0], "var"))
                stmtList.append(Stmt(lineNum, keyword, exprList))


# found on StackOverflow
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?rq=1
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def executeStmts(lineNum, symTable, labelTable, stmtList):
    for x in stmtList[(lineNum - 1):(len(stmtList))]:
        x.perform(symTable, labelTable, stmtList)
    
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
#! /usr/bin/env python3
import fileinput
import sys

# used to store a parsed TL expressions which are
# constant numbers, constant strings, variable names, and binary expressions
class Expr:
    def __init__(self,op1,operator,op2=None):
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
    def __init__(self,lineNum,keyword,exprs):
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
        print ("Doing: " + str(self))

# read 1st argument when calling script
fileName = sys.argv[1]

# open file with given filename
file = open(fileName, "r")

lineNum = 0
symTable = {}
stmtList = []
def addStmt(stmtList, lineNum, keyword, lineParsed, stInd, endInd):
    stmtList.append(Stmt(lineNum, keyword, lineParsed[stInd:endInd]))

for x in file:
    labelIndex = 0
    lineNum += 1
    lineParsed = x.split()
    numTokens = len(lineParsed)
	
    # check if there is a label
    if lineParsed[0].endswith(':'):
        # store label without colon
        symTable[lineParsed[0][:-1]] = lineNum
        # rest of statement will start one index over
        labelIndex = 1
		
    keyword = lineParsed[0 + labelIndex]
    if keyword == "let":
        addStmt(stmtList, lineNum, keyword, lineParsed, (1 + labelIndex), numTokens)
        # stmtList.append(Stmt(lineNum, keyword, lineParsed[(1 + labelIndex):(numTokens)]))
    elif keyword == "if":
        addStmt(stmtList, lineNum, keyword, lineParsed, (1 + labelIndex), numTokens)
        # stmtList.append(Stmt(lineNum, keyword, lineParsed[(1 + labelIndex):(numTokens)]))
    elif keyword == "print":
        addStmt(stmtList, lineNum, keyword, lineParsed, (1 + labelIndex), numTokens)
        # stmtList.append(Stmt(lineNum, keyword, lineParsed[(1 + labelIndex):(numTokens)]))
    elif keyword == "input":
        addStmt(stmtList, lineNum, keyword, lineParsed, (1 + labelIndex), numTokens)
        # stmtList.append(Stmt(lineNum, keyword, lineParsed[(1 + labelIndex):(numTokens)]))
	
for x in symTable:
    print(str(symTable[x]))
for x in stmtList:
    print(str(x))
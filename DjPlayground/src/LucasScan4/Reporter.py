'''
Created on Jan 29, 2014

@author: McChimp
'''        

class TableTransaction:
    def __init__(self, secTitle, secDate, secCode, secAmount, secAorD, secOwnedAfter, secPrice, tableType):
        """TODO:add ownedAfter into DB"""
        self.title  = secTitle
        self.date   = secDate
        self.code   = secCode
        self.amount = secAmount
        self.AorD   = secAorD
        self.ownedAfter = secOwnedAfter
        self.price  = secPrice
        self.type   = tableType

class Reporter:
    def __init__(self, Title, Link, Date, XMLLink, HTMLLink):
        self.title = Title
        self.date  = Date
        self.link  = Link
        self.xmlLink = XMLLink
        self.htmLink = HTMLLink
        self.table1 = []
        self.table2 = []
        
    def enterSymbol(self, Symbol):
        self.symbol = Symbol
    
    def enterReporter(self, Title, Name, isDirector): 
        """TODO:add director to DB"""
        self.officerTitle = Title
        self.officerName  = Name
        self.director = isDirector
    
    def enterT1Transaction(self, TableTransaction):
        self.table1.append(TableTransaction)

    def enterT2Transaction(self, TableTransaction):
        self.table2.append(TableTransaction)
        
    def generateSummary(self):
        """Calculates totals owned by Reporter, saves transaction codes and totals in Reporter Object"""
#        """TODO: split table by title, calculate before and after, save into list, insert list into DB"""
#        """TODO: add totals and codes into DB"""
#         if(self.table1 == []):
#             self.nonDerivativeOwnedBefore = None
#         else:
#             if(self.table1[0].AorD == 'A'):
#                 self.nonDerivativeOwnedBefore = float(self.table1[0].ownedAfter) - float(self.table1[0].amount)
#             if(self.table1[0].AorD == 'D'):
#                 self.nonDerivativeOwnedBefore = float(self.table1[0].ownedAfter) + float(self.table1[0].amount)
#             self.TotalNonDerivativeOwnedAfter = float(self.table1[-1].ownedAfter)
# 
#         if(self.table2 == []):
#             self.derivativeOwnedBefore = None
#         else:
#             if(self.table2[0].AorD == 'A'):
#                 self.derivativeOwnedBefore = float(self.table2[0].ownedAfter) - float(self.table2[0].amount)
#             if(self.table2[0].AorD == 'D'):
#                 self.derivativeOwnedBefore = float(self.table2[0].ownedAfter) + float(self.table2[0].amount)
#             self.TotalDerivativeOwnedAfter = self.table2[-1].ownedAfter
        
        self.t1TotalA = 0
        self.t1codesA = ''
        self.t1TotalD = 0
        self.t1codesD = ''
        self.t2TotalA = 0
        self.t2codesA = ''
        self.t2TotalD = 0
        self.t2codesD = ''
        for ta in self.table1:
            if(ta.AorD == "A" or ta.AorD == "a"):
                self.t1TotalA += float(ta.amount)
                self.t1codesA += str(ta.code)
            if(ta.AorD == "D" or ta.AorD == "d"):
                self.t1TotalD += float(ta.amount)
                self.t1codesD += str(ta.code)
        for ta in self.table2:
            if(ta.AorD == "A" or ta.AorD == "a"):
                self.t2TotalA += float(ta.amount)
                self.t2codesA += str(ta.code)
            if(ta.AorD == "D" or ta.AorD == "d"):
                self.t2TotalD += float(ta.amount)
                self.t2codesD += str(ta.code)
        
    def convertTimeStamp(self):
        pass
    
    def oneRowString(self):
        s = self.symbol+"\t"+str(self.t1TotalA)+"\t"+self.t1codesA+"\t"+str(self.t1TotalD)+"\t"+self.t1codesD+"\t"+str(self.t2TotalA)+"\t"+self.t2codesA+"\t"+str(self.t2TotalD)+"\t"+self.t2codesD+"\t"+self.date+"\t"+self.title+"\t"+str(self.director)+"\t"+self.officerTitle+"\t"+self.officerName+"\t"+self.htmLink
        return s
        
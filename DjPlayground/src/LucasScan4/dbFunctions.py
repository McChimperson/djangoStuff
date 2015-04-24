'''
Created on Feb 22, 2014

@author: McChimp
'''
import sqlite3
import os

conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS reporters
             (timestamp text, 
              symbol text, 
              officertitle text,
              officername text, 
              title text,
              isDirector text, 
              hlink text, 
              xlink text, 
              pnlink text,
              id integer PRIMARY KEY)''')

c.execute('''CREATE TABLE IF NOT EXISTS transactions(
              timestamp text,
              symbol text,
              aord text,
              stockordv text,
              amount real,
              code text,
              ownedAfter text,
              price real,
              title text,
              id integer PRIMARY KEY,
              FOREIGN KEY(timestamp,symbol) REFERENCES reporters(timestamp,symbol))''')
conn.commit()

def closeConnection():
    conn.close()

def appendDB(ReporterList):
    for pn in ReporterList:
        pnTimestamp  = pn.date
        symbol       = pn.symbol
        officerTitle = pn.officerTitle
        officerName  = pn.officerName
        isDirector   = pn.director
        pnTitle      = pn.title
        htmLink      = pn.htmLink
        xmlLink      = pn.xmlLink
        pnLink       = pn.link
        c.execute('''INSERT INTO reporters VALUES(?,?,?,?,?,?,?,?,?,NULL)''',
                 (pnTimestamp, symbol, officerTitle, officerName, pnTitle, isDirector, htmLink, xmlLink, pnLink))
        for stTa in pn.table1:
            taTimestamp = stTa.date
            rpSymbol    = pn.symbol
            taAorD      = stTa.AorD
            taStockorDv = stTa.type
            taAmount    = stTa.amount
            taCode      = stTa.code
            taOwnedAfter= stTa.ownedAfter
            taPrice     = stTa.price
            taTitle     = stTa.title
            c.execute('''INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,NULL)''',
                     (taTimestamp, rpSymbol, taAorD, taStockorDv, taAmount, taCode, taOwnedAfter, taPrice, taTitle))
        for dvTa in pn.table2:
            taTimestamp = dvTa.date
            rpSymbol    = pn.symbol
            taAorD      = dvTa.AorD
            taStockorDv = dvTa.type
            taAmount    = dvTa.amount
            taCode      = dvTa.code
            taOwnedAfter= dvTa.ownedAfter
            taPrice     = dvTa.price
            taTitle     = dvTa.title
            c.execute('''INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,NULL)''',
                     (taTimestamp, rpSymbol, taAorD, taStockorDv, taAmount, taCode, taOwnedAfter, taPrice, taTitle))
    conn.commit()
    
def txtPath():
    #path must be hard coded for Windows Task Scheduler
    #p += "C:\\Users\\McChimp\\Google Drive\\LucasScan4.01\\src\\form4.txt"
    p = os.getcwd()
    p += "\\form4.txt"
    p = p.replace('\\','/')
    return p
    
def textDate():
    p = txtPath()
    with open(p, "r") as permList:
        fl = permList.readline()
    permList.close()
    if(fl == ""):
        return None
    flp = fl.split('\t')
    return flp[9]

def textPrepend(ReporterList):
    p = txtPath()
    with open(p, "r") as permList:
        tail = permList.read()
    permList.close()
    with open(p, "w") as permList:
        for pn in ReporterList:
            permList.write(pn.oneRowString()+"\n")
        permList.write(tail)
    permList.close()
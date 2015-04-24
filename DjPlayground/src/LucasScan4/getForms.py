'''
Created on Jan 29, 2014

@author: McChimp
'''

import urllib.request
import re
from bs4      import BeautifulSoup
from Reporter import Reporter, TableTransaction

domain   = "http://www.sec.gov"

def trimRSSlist(entryList, stopTime):
    count = 0
    if (stopTime == []):
        print("No StopTime Given")
        return entryList
    for e in entryList:
        entryTime = str(e.contents[7].string)
        if(entryTime == stopTime):
            print(str(stopTime) + " matched: " + str(count/2) + " new entries found")
            return entryList[:count]
        count += 1
    print(str(stopTime) + " not found")
    print(str(count/2) + " new entries found")
    return entryList

def processRSS(stopTime):
    '''return soup of entries of RSS''' 
    startNum = 0
    RSSUrl   = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&company=&dateb=&owner=only&start=" + str(startNum) + "&count=100&output=atom"
    entryList = []
    while(startNum <= 200): 
        response    = urllib.request.urlopen(RSSUrl)
        soup        = BeautifulSoup(response.read())
        workingList = soup.find_all("entry")
        startNum = startNum + 100
        RSSUrl   = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&company=&dateb=&owner=only&start=" + str(startNum) + "&count=100&output=atom"
        for e in workingList:
            entryList.append(e)
            if(str(e.contents[7].string) == stopTime):
                break
    return entryList
        

def getForms(entrySoup):
    '''Takes input as RSS Soup and returns a Reporter object with
       name, wrapper Link, date. Parses wrapper site and gets XMLlink and HTMLlink'''
    t = entrySoup.title.string
    l = entrySoup.link.attrs['href']
    d = entrySoup.updated.string
    '''Next site retrieval and parse'''
    rsp = urllib.request.urlopen(l)
    sp  = BeautifulSoup(rsp.read()) 
    '''Find First Table and Extract Rows and 3rd Column'''
    rows = sp.find_all('table')[0].find_all('tr')
    del rows[0]     #get rid of header
    col3 = []       #column 3 contains needed links
    for row in rows:
        col3 += row.findAll('td')[2].contents
    x = domain + col3[1].attrs['href']
    h = domain + col3[0].attrs['href']
    return Reporter(t,l,d,x,h)

def parseForm(pn):
    """Take Reporter, Open Reporter.xmlLink, append data to Reporter in TableTransaction"""
    response = urllib.request.urlopen(pn.xmlLink)
    soup = BeautifulSoup(response.read())
    sym = soup.issuertradingsymbol.string
    director = False
    if(soup.isdirector != None):
        if(soup.isdirector.string in [True, 1, "True", "1"]): director = True
        else: director = False
    officerTitle = "No Title"
    if(soup.isofficer != None):
        if(soup.isofficer.string in [True, 1, "True", "1"]): officerTitle = soup.officertitle.string
        else: officerTitle = "No Title"
    officerName  = soup.rptownername.string
    pn.enterSymbol(sym)
    pn.enterReporter(officerTitle, officerName, director)
    
    table1soup = soup.find_all("nonderivativetransaction")
    for ndta in table1soup:
        title1 = ndta.securitytitle.value.string
        date1  = pn.date
        code1  = ndta.transactioncode.string
        amnt1  = ndta.transactionshares.value.string
        AorD1  = ndta.transactionacquireddisposedcode.value.string
        if(ndta.sharesownedfollowingtransaction):
            amntAfter1 = ndta.sharesownedfollowingtransaction.value.string
        else: amntAfter1 = 0
        if(ndta.transactionpricepershare == None): price1 = 0
        else:
            if(ndta.transactionpricepershare.value == None): price1 = 0
            else:                                            price1 = ndta.transactionpricepershare.value.string
        transaction1 = TableTransaction(title1, date1, code1, amnt1, AorD1, amntAfter1, price1, 1)
        pn.enterT1Transaction(transaction1)
    table2soup = soup.find_all("derivativetransaction")
    for dta in table2soup:
        title2 = dta.securitytitle.value.string
        date2  = pn.date
        code2  = dta.transactioncode.string
        if(dta.transactionshares == None): amnt2 = 0
        else:                              amnt2  = dta.transactionshares.value.string
        AorD2  = dta.transactionacquireddisposedcode.value.string
        if(dta.sharesownedfollowingtransaction):
            amntAfter2 = dta.sharesownedfollowingtransaction.value.string
        else: amntAfter2 = 0
        if((dta.conversionorexerciseprice == None) or (dta.conversionorexerciseprice.footnoteid)): price2 = 0
        else:                                      price2 = dta.conversionorexerciseprice.value.string
        transaction2 = TableTransaction(title2, date2, code2, amnt2, AorD2, amntAfter2, price2, 2)
        pn.enterT2Transaction(transaction2)
    
def go(entryList):
    """Takes list of entries from processRSS"""
    ReporterList = []
    for tag in entryList:
        '''Discard Reporter Filings'''
        if(re.search('(Reporting)', tag.title.string)):
            continue
        reporter = getForms(tag)
        parseForm(reporter)
        reporter.generateSummary()
        ReporterList.append(reporter)
        print(reporter.oneRowString())
    return ReporterList

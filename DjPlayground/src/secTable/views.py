from django.shortcuts import render

# Create your views here.
import pytz
from datetime import datetime, timedelta
from dateutil import parser
from django.http import HttpResponse
from django.utils import timezone
from secTable.models import Reporters, Transactions

#request handlers


def grabAll(request):
    all_reporters   = Reporters.objects.all()
    all_transations = Transactions.objects.all()
    test_list   = buildTestList(all_reporters, all_transations)
    #combinedList = list(chain(all_reporters, all_transations))
    return HttpResponse(test_list)

def grabByDate(request):
    est = pytz.timezone('EST')
    
    if("symbol" not in request.GET):
        sym = -1
    else:
        sym = request.GET["symbol"]
        if(sym[-1] == '/'):
            sym = sym[:-1]
        
    if("startDate" not in request.GET):
        start_date_object = datetime.now()
        start_date_object = timezone.make_aware(start_date_object, est)
    else:
        startString = request.GET["startDate"]
        if(startString[-1] == '/'):
            startString = startString[:-1]
        start_date_object = parseDateString(startString)
        
    if("endDate" not in request.GET):
        #end_date_object = datetime.now()+timedelta(days=1)
        end_date_object = datetime.now()-timedelta(days=30)
        end_date_object = timezone.make_aware(end_date_object, est)
    else:
        endString = request.GET["endDate"]
        if(endString[-1] == '/'):
            endString = endString[:-1]
        end_date_object = parseDateString(endString)
        
    if(sym == -1):
        reporterQuerySet = Reporters.objects.filter(
            timestamp__lt  = start_date_object,
            timestamp__gte = end_date_object)
    
        transactionQuerySet = Transactions.objects.filter(
            timestamp__lt  = start_date_object,
            timestamp__gte = end_date_object)
    else:
        reporterQuerySet = Reporters.objects.filter(
            symbol         = sym,
            timestamp__lt  = start_date_object,
            timestamp__gte = end_date_object)
    
        transactionQuerySet = Transactions.objects.filter(
            symbol         = sym,
            timestamp__lt  = start_date_object,
            timestamp__gte = end_date_object)
        
    tableEntryList = []
    for r in reporterQuerySet:
        tQuerySet = getTransactions(r, transactionQuerySet)
        tblEntry = TableEntry(r, tQuerySet)
        #blEntry = tblEntry.generateSummary()
        tableEntryList.append(tblEntry)
        
    context_instance = {'tableEntryList':tableEntryList}
    
    return render(request, "table.html", context_instance)

#utils

class TableEntry():
    def __init__(self, r, tQS):
        self.reporter = r
        self.transactions = tQS
        
        self.t1TotalA = 0
        self.t1codesA = ''
        self.t1TotalD = 0
        self.t1codesD = ''
        self.t2TotalA = 0
        self.t2codesA = ''
        self.t2TotalD = 0
        self.t2codesD = ''
        
        for t in self.transactions:
            if t.stockordv == "1":
                if(t.aord == "A" or t.aord == "a"):
                    self.t1TotalA += float(t.amount)
                    self.t1codesA += str(t.code)
                if(t.aord == "D" or t.aord == "d"):
                    self.t1TotalD += float(t.amount)
                    self.t1codesD += str(t.code)
            if t.stockordv == "2":
                if(t.aord == "A" or t.aord == "a"):
                    self.t2TotalA += float(t.amount)
                    self.t2codesA += str(t.code)
                if(t.aord == "D" or t.aord == "d"):
                    self.t2TotalD += float(t.amount)
                    self.t2codesD += str(t.code)
        
        if(self.t1codesA == ''):self.t1codesA='-'
        if(self.t1codesD == ''):self.t1codesD='-'
        if(self.t2codesA == ''):self.t2codesA='-'
        if(self.t2codesD == ''):self.t2codesD='-'
    
def getTransactions(r, tQuerySet):
    '''return a Queryset containing all of a single reporter object's associated transaction objects from a Transaction QuerySet'''
    rsTransactons = tQuerySet.filter(timestamp__startswith = r.timestamp)
    return rsTransactons

def parseDateString(dtString):
    '''input dateString, return dateTime object'''
    dt = parser.parse(dtString)
    return(dt)

def buildTestList(reporterQuerySet, transactionQuerySet):
    '''querySets are the input'''
    #pdb.set_trace()
    completeList = ''
    for r in reporterQuerySet.all():
        #print(r.timestamp)
        completeList += r.symbol + ",&nbsp;" + r.officertitle + ",&nbsp;" + r.isdirector + ",&nbsp;" + r.officername + ",&nbsp;" +  r.timestamp + "<p>"
        filteredlist = transactionQuerySet.filter(timestamp = r.timestamp)
        for t in filteredlist:
            #print("\t" + t.timestamp)
            completeList += str("&nbsp;&nbsp;&nbsp;&nbsp;"+t.title+",&nbsp;"+t.aord+",&nbsp;"+str(t.amount)+",&nbsp;"+t.code+",&nbsp;"+str(t.ownedafter)+"<p>")
    print(completeList)
    return completeList
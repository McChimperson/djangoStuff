'''
Created on Jan 29, 2014

@author: McChimp
'''

import sys
from time import sleep
import getForms
import dbFunctions

if __name__ == '__main__':
    stopTime = dbFunctions.textDate()
    rssSoupList = getForms.processRSS(stopTime)
    rssSoupList = getForms.trimRSSlist(rssSoupList, stopTime)
    if(rssSoupList == []):
        print("No new entries")
        sleep(3)
        sys.exit()
    print("symbol"+"\t"+
          "t1TotalA"+"\t"+
          "t1codesA"+"\t"+
          "t1TotalD"+"\t"+
          "t1codesD"+"\t"+
          "t2TotalA"+"\t"+
          "t2codesA"+"\t"+
          "t2TotalD"+"\t"+
          "t2codesD"+"\t"+
          "date"+"\t"+
          "title"+"\t"+
          "officerTitle"+"\t"+
          "isDirector"+"\t"+
          "officerName"+"\t"+
          "link")
    reporterList = getForms.go(rssSoupList)
    dbFunctions.appendDB(reporterList)#
    dbFunctions.textPrepend(reporterList)#
    dbFunctions.closeConnection()
    print('\n-----------------------COMPLETE-----------------------\n')
    sleep(3)
    pass 

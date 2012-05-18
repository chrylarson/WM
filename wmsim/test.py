#-------------------------------------------------------------------------------
# Name:        test
# Purpose:
#
# Author:      Administrator
#
# Created:     17/05/2012
# Copyright:   (c) Administrator 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import datetime

def now():
    tmp = datetime.datetime.now()
    return ( (tmp.day * 24 * 60 * 60 + tmp.second) * 1000 + tmp.microsecond / 1000.0)

def testTimeOut():
    t = 0
    esci = 0
    n = now()
    t = now()

    while esci==0:
        if (t-n) > 5000:
            esci = 1
        else:
            print"time", (t-n)
            t = now()

class A:
    x = []
    y = 0
    def add(self):
        self.x.append(1)
        self.y +=1

class B:
    def __init__(self):
        self.x = []

    def add(self):
        self.x.append(1)

class C(B):
    def Add2(self):
        self.add()
        self.x.append(1)




def main():
    #testTimeOut()

    x = A()
    x.add()
    x.add()
    print "A's x:",x.x, x.y
    y = A()
    y.add()
    print "A's x:",x.x, x.y
    print "A's y:",y.x, y.y
    x = B()
    y = B()
    z = C()
    x.add()
    y.add()
    z.Add2()
    print "B's x:",x.x
    print "C's x:",z.x

if __name__ == '__main__':
    main()

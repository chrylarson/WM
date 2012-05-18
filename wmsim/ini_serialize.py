#/usr/bin/env python
import sys,os,datetime,time,re,string
from StringIO import StringIO
from ConfigParser import ConfigParser


GREP_NEGATIVE=True

def grep (str_list,pattern,neg=False):
    """grep() will return list of match case.
Param: str_list - must be a list of string, each element in list is a new line
                  can use .split('\n') to obtain list from mutiple line of string
Param: pattern - re pattern can be composed by re.compile()"""
    sres=[] #empty list
    for s in str_list:
        r=re.search(pattern,s,re.VERBOSE)
        if r and neg==False:
            sres.append(s)
        elif (not r) and neg==True:
            sres.append(s)

    return sres

def ParseConfig (name=None):
    global GREP_NEGATIVE
    """ Parsing config file to this function, will serialized to dictionary
@name  = filename
@return = dictionary"""
    configdict={}
    loglist=[]

    while True:
        try:
            f = open(name,"r")
        except IOError:
            print "Err ",name,"not exist"
            return None
            pass
        else:
            break

    try:
        for line in f:
            #strip all the whitespaces and write all lines to list.
            loglist.append(line.strip(string.whitespace))
    finally:
        f.close()

    # filter out the comment
    loglist=grep(loglist,"^\#",GREP_NEGATIVE)

    # make a dictionary
    xL=[] #current L
    itemdict={}
    for item in loglist:
        L=grep([item],"^\[.*\]$") # section
        if L:
            xL=[L[0].lstrip("[").rstrip("]")]
            itemdict={}
            #print xL
        else: # items?
            if len(xL)>0:
               if item:
                    #split index and values.
                    iL=item.split("=")
                    #replace all '\t' to " " in values
                    iL[1]=string.replace(iL[1],"\t"," ")
                    # split the values into list
                    iiL=iL[1].strip(string.whitespace).split(" ")
                    real_list=[]
                    for item in iiL:
                        # read each value in the list, if got something append to the real_list
                        if len(item.strip(string.whitespace)) is not 0:
                            real_list.append(item.strip(string.whitespace))
                    # create another dict into the section
                    itemdict[iL[0].strip(string.whitespace)]=real_list
                    configdict[xL[0]]=itemdict
    return configdict
pass

def ConfigTemplate (name=None):
    try:
        f=open(name,"r")
    except IOError:
        return None

    loglist=[]
    try:
        for line in f:
            #strip all the whitespaces and write all lines to list.
            theline = line.strip(string.whitespace)
            loglist.append(theline)
    finally:
        f.close()

    loglist=grep(loglist,"^\#|^\[")
    if len(loglist) is 0:
        loglist = None
    return loglist

def ConfigWrite (template=[],config=[],filename=""):
    global DebugDupConfigWrite

    if len(template) is 0 or len(config) is 0 or filename is "":
        return False

    try:
        f = open(filename,"w")
        for line in template:
            r=re.search("^\#",line,re.VERBOSE)
            if r:
                f.write(line + "\n")
            j=re.search("^\[",line,re.VERBOSE)
            if j:
                f.write(line + "\n")
                # get all section line up
                section_name = line.strip(string.whitespace).lstrip("[").rstrip("]")
                if config.has_key(section_name):
                    sec_dict = config[section_name]
                    #
                    element_list=[]
                    for element in sec_dict:
                        element_list.append(element)
                    element_list.sort()
                    for element in element_list:
                        # index = values....
                        #print element, sec_dict[element]
                        f.write(element + " = " + "\t".join(sec_dict[element]) + "\n")
                    f.write("\n")
                else:
                    pass
                    #f.write("CAN'T FIND THE ELEMENTS in section[%s]! DATA CORRUPTED.\n" % section_name)
                pass # end if j

            pass # end for line
        f.close()
        return True

    except:
        return False

# sample calling
myDict = ParseConfig ("test_config.ini")
template = ConfigTemplate ("test_config.ini")
ConfigWrite(template,myDict,"test_test.ini")

print "COMPLETE DICTIONARY"
print myDict

print "ALL TAGS"
for c in myDict:
    print " ",c

print ""
print "ALL ITEM IN 'GENERAL'"
for d in myDict["GENERAL"]:
    print " ",d

print ""
print "ALL ITEM IN 'LOG'"
for d in myDict["LOG"]:
    print " ",d

print ""
print "DIRECT ACCESS 'LOG's LOGTYPE'"
print myDict["LOG"]["LogType"]

print "SO, YOU CAN SEE THAT IS THE LIST, IT ITERATE the LIST"
for e in myDict["LOG"]["LogType"]:
    print " ",e

print "DIRECT ACCESS 'LOG's LOGTYPE 2nd value'"
print "second value is ",myDict["LOG"]["LogType"][1]


# from list to dictionary
l = myDict["DEV"]["sta_1"]
print l
d = dict([(k, v) for k,v in zip (l[::2], l[1::2])])
print d

ini = ConfigParser()
ini.read('test_config.ini')

myTagDic = ini._sections['DEV']
print myTagDic
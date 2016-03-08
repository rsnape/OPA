'''
Created on 15 May 2013

@author: jsnape

takes a file with first line as reference (or simulation) output

all other lines observations.

Produces stats of misses, hits, ties and other metrics as per Thorngate and Edmonds 2013 for each line
'''
import random

def getPairs(myList):
    listLen = len(myList)
    retList = []
    for i in xrange(len(myList),0,-1):
        n=myList[i-1]
        for j in xrange(i,0,-1):
            if myList[j-1] < n:
                retList += [i-1,j-1]
    return retList

def OPA_analyse(predictions,observations):
    numPairs = len(predictions)/2
    hits = 0 
    ties = 0 
    misses = 0
    NAs = 0
    for test in xrange(numPairs):
        a=predictions[test+test]
        b=predictions[test+test+1]
        if observations[a] == "NA" or observations[a] == "" or observations[b] == "NA" or observations[b] == "":
            NAs+=1
        elif observations[a] > observations[b]:
            hits+=1
        elif observations[a] == observations[b]:
            ties+=1
        elif observations[a] < observations[b]:
            misses+=1  
    
    return (hits,misses,ties,NAs)    

def rowToList(l):
    l=l.strip('\n')
    l=l.split(",")
    for (i,n) in enumerate(l[1:]):
        if n!="NA":
            l[i+1]=int(n)
    return l
    
def OPA_display(statSet):
    if statSet[0]+statSet[1] == 0:
        PM = None
        IOF = None
    else:
        PM = statSet[0]*1.0/(statSet[0]+statSet[1])
        IOF = PM+PM-1
    
    print "Matches\t:",statSet[0]
    print "MisMatches\t:",statSet[1]
    print "Ties\t:",statSet[2],"; NAs\t\t:",statSet[3]
    print "PM (Probability of a match) =",PM
    print "IOF (Index of observed fit) =",IOF
    
    return IOF
    
def bootstrapResample(myList,n=None):
    l=len(myList)
    if not n:
        n=l
    res=[]
    for i in xrange(n):
        a=myList[random.randint(0,l-1)]
        res.append(a)
    return res

nSample = 200
simLabel=""
#f=open("Dataset.csv",'r+')
#f=open("Trends_per_postcode_for_OPA.csv",'r+')
#f=open("trends_post_apr_2010_for_OPA.csv",'r+')
f=open("trends_post_apr_2010_for_OPA.csv",'r+')
fnotSame = open ("PCode_OPA_overP.csv",'w')
fSimilar = open("PCode_OPA_underP.csv",'w')

largePVals=[]
firstLine=True
for l in f:
    l=rowToList(l)
    label=l[0]
    l=l[1:]
    if firstLine:
        preds = getPairs(l)
        simLabel=label
        #print preds
        firstLine = False
    else:
        stats=OPA_analyse(preds,l)
        print "OPA stats for",label,"vs.",simLabel
        IOF=OPA_display(stats)
        exceeds=0
        r=l
        if nSample > 0:
            for i in xrange(nSample):
                r = random.sample(l,len(l))#bootstrapResample(l)
                nStat = OPA_analyse(preds,r)
                if nStat[0] >= stats[0]:
                    exceeds+=1
            p=exceeds*1.0 / nSample
            print "P(Number of matches >= obtained matches) =",p
            if p>0.05:
                fnotSame.write(label+":"+str(p)+";IOF="+str(IOF)+"\n")
            else:
                fSimilar.write(label+":"+str(p)+";IOF="+str(IOF)+"\n")
    
        
    
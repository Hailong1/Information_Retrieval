#python 3.7
"""

@author: hailong
"""

import re
import os
import collections
import time
import math
import string
import random

class index:
    
    def __init__(self,path):
        
        self.path=path
        self.doc={} # contain the documents and their document id
        #self.document={} 
        self.docwidf={} # contain the terms and posting list in 
                        # the index. 
        self.docWhole={}   # contain the whole context of this id.              
       
    def buildIndex(self):
        
        start=time.time()
        paths=self.path+"\collection"
        files=os.listdir(paths)
        # above method is use to scan the context of this directory.
        doc=self.doc
        #document=self.document
        doc_id=1 # the number for the ducument text, ducument id.
                 # final it will the number of the textfile
                 # that is N
        count=0 # this is used to record the location in the text. 
        docwidf=self.docwidf
             # it map all exceptthe idf and tf  
        #num=0 
        docWhole=self.docWhole
        for file in files:
            doc[doc_id]=file         
            road=paths+"\\"+file
            # this is the path to find each text.
            f=open(road,"r")
            road=paths
            whole=""
            list1=[] # in this list in store three element one is 
                 # id1, one is wtd,one is postion. 
            stop=["a","an","and","are","as","at",\
                  "be","by","for","from","has","he","in",\
                  "is","it","its","of","on","that","the",\
                  "to","was","were","will","with"]
            for line in f.readlines():
                line=line.lower()                  
               # whole=whole+line
                word=line.split()                 
                for w1 in word:
                   count=count+1
                   match=re.search("[a-z][a-z'.]*[a-z]?",w1)
                   pos=""
                     # basic tokenization. remove all punctuations
                     # between the two words, and remove numerals.
                   if match!=None: 
                       sigword=match.group() 
                       if sigword not in stop: 
                           
                            whole=whole+sigword
                            # read the whole context except the 
                            # stop word and the unmathched words. 
                            sigword=sigword+":[idf" 
                            list1.append(str(doc_id))
                            temp="wtd-"+str(doc_id)
                            list1.append(temp)
                            if  not docwidf.__contains__(sigword):                              
                                pos=str(count)                         
                                list1.append(pos)
                                docwidf[sigword]=[]  
                                docwidf[sigword].append([list1[0]
                                           ,list1[1],list1[2]]) 
                                list1.clear()
                            else:
                                
                                num=len(docwidf[sigword])-1
                                flag="0"
                                for v in docwidf[sigword]:
                                    if v[0]==str(doc_id):
                                       # print(sigword,":",v[0])
                                        temp1=docwidf[sigword][num][2]\
                                           +","+str(count)
                                        list1.append(temp1)
                                        temp1=""
                                        docwidf[sigword][num].clear()
                                    
                                        docwidf[sigword][num]=\
                                        [list1[0],list1[1],list1[2]]
                                        flag="1"
                                        break
                                if flag=="0":          
                                   pos=str(count)
                                   list1.append(pos)
                                   docwidf[sigword].append([list1[0]
                                           ,list1[1],list1[2]]) 
                                list1.clear()                                                 
          
            count=0  
            docWhole[doc_id]=whole
            doc_id=doc_id+1
            
        docwidf=self.find_wtd_idf(doc_id,docwidf) 
        
        end=time.time()       
        bpath=self.path
        bpath=bpath+"\Output.txt"
        bf=open(bpath,"w")
        bftemp="Index built in "+str(end-start)+" seconds \n\n"
        bf.write(bftemp)
        bf.close()      
        
        print('Index built in %s seconds'%(end-start))
    
    
    # find the idf and wtd. 
    def find_wtd_idf(self,n,doc):
        tf=0 # the value of the tf for each document.
        df=0 # the vlue of the df for the term.
        idf=0 # the vlue of the idf for the term
        wtd=0 # the value of the wtd for the document.
        n=n-1
        #doc=self.docwidf
        for key in doc:
           # print(num)            
            p=0
            while p<len(doc[key]):
              # print(len(doc[key])) 
               docu_id=doc[key][p][0] 
               pos=doc[key][p][2]
               if "," in pos:
                   plist=pos.split(",")
                   tf=len(plist)                  
               else: 
                   tf=1
               wtd=1+math.log10(tf)
               wtd=round(wtd,3)
               doc[key][p].clear()
               doc[key][p]=[docu_id,str(wtd),pos]
               p=p+1 
               
        for key1 in doc:               
            df=len(doc[key1])
            idf=math.log10(n/df)
            idf=round(idf,3)
            change=key1.split("[")
            newkey=change[0]+"["+str(idf)
            doc[newkey]=doc.pop(key1)
            
        for key1 in doc:
            df=len(doc[key1])
            if "idf" in key1:
                change=key1.split("[")
                idf=math.log10(n/df)
                idf=round(idf,3)
                change=key1.split("[")
                newkey=change[0]+"["+str(idf)
                doc[newkey]=doc.pop(key1)    
        return doc 
        
        
    def exact_query(self,query_terms,k):
        exstart=time.time()
        doc=self.docwidf
        qlist=query_terms.split()
        #qdoc={} # first store tf-idf vlue about key ducument 
                # then store the unit vector for key document
        #tdoc={} 
        qdoc,tdoc=self.find_idf_To_Vector(qlist,doc,"idf")
        
        qdoc,tdoc=self.find_unit_Vector(qdoc,tdoc)
                                   
        result=self.cos(qdoc,tdoc,k)

        top="the exact Top "+str(k)+" query result for the "+\
               query_terms+" is below:\n\n"
            
        exend=time.time()
    
        late="exact_query use "+str(exend-exstart)+" seconds \n\n"
        self.printTo(top,late,result)
        
        print('exact_query use %s seconds'%(exend-exstart))
     
    
        #find unit vector。
    def find_unit_Vector(self,qdoc,tdoc):
                
        temp1=[] # store the value about tf_idf 
        
        #find the query unit vector。          
        for qkey in qdoc:
            temp1.append(qdoc[qkey])            
        result=0    
        for v in temp1:
            temp2=v*v
            result=result+temp2
        finalresult=math.sqrt(result)
        finalresult=round(finalresult,3)
        temp1.clear()
        for qkey in qdoc:
            vectorvalue=qdoc[qkey]/finalresult
            vectorvalue=round(vectorvalue,3)
            qdoc[qkey]=vectorvalue    
       ## after above the qdoc store the unit vector value         
        
       #find the document unit vector。
        for qkey in tdoc:
            temp1.append(tdoc[qkey])            
        result=0    
        for v in temp1:
            temp2=v*v
            result=result+temp2
        finalresult=math.sqrt(result)
        finalresult=round(finalresult,3)
        temp1.clear()
        for qkey in tdoc:
            vectorvalue=tdoc[qkey]/finalresult
            vectorvalue=round(vectorvalue,3)
            tdoc[qkey]=vectorvalue
        # after above the qtoc store the unit vector value   
        
        return qdoc,tdoc
       
        
    # get the cos    
    def cos(self,query,doc,k):
        
        scoredic={}       
        for d in doc:
            score=0
            for q in query:
                   score=score+query[q]*doc[d] 
                   score=round(score,3)
            scoredic[d]=score 
       
        TopK=sorted(scoredic, key=lambda key: scoredic[key])
        ## above a function sort the map according to the value
        ## result is a list about the key increasing order
           
        resultlist=self.getTop(TopK,k)
        return resultlist
     
     
     ## get the top list. 
        
    def getTop(self,TopK,limit):
         
        resultlist=[]
        i=len(TopK)-1
        num=1
        while i>=0:            
           if num<=limit: 
             resultlist.append(TopK[i])
             num=num+1
           i=i-1          
        
        return resultlist
    
    ## print to the query to the txt.
     
    def printTo(self,top,late,result):   
        
        pdlpath=self.path  
        pdlpath=pdlpath+"\Output.txt"
        docu=self.doc
        qf=open(pdlpath,"a")      
        qf.write(top)
        if result:
            for r in result:
                for doc in docu:
                    
                    if  r==str(doc):
                        #print(doc)
                        temp=docu[doc]+"\n"
                        qf.write(temp)
                        temp=""
                        break
            # below is means the result is empty.            
        else:
            qf.write("search are not find in document\n")
        qf.write(late)
        qf.close()
      
    # find the tf-idf of the vector
    # or find the wtd of the vector
    # according to the parameter choice
    def find_idf_To_Vector(self,qlist,doc,choice):
            
        qdoc={}
        tdoc={}
        wdoc={} # return the doc_id and its wtd.
        for value in qlist:           
            for key in doc:
                temp200=key.split("[")
                term=temp200[0]
                term=term.strip(string.punctuation)
                # delete the ending punctuation
                if str(value)==term:
                    #print(value)
                    temp=key.split("[")
                    value100=temp[1]
                    idf=float(value100)
                    tf_idfq=idf*1 # the value accur in query only once
                    qdoc[value]=tf_idfq
                    p=0
                    while p<len(doc[key]):
                        doc_id=doc[key][p][0]
                        value1=float(doc[key][p][1])
                        wdoc[doc_id]=value1
                        tf_idft=idf*value1
                        tdoc[doc_id]=tf_idft
                        p=p+1
        if choice=="idf":   
           return qdoc,tdoc
        if choice=="wtd":
           return qdoc,wdoc 
        
        
        
    def inexact_query_champion(self,query_terms,k):
        IneCstart=time.time()
        doc=self.docwidf
        qlist=query_terms.split()
        
        qdoc,tdoc=self.find_idf_To_Vector(qlist,doc,"wtd")
        
        if len(tdoc)<=30: # it is mean all all words contain few 
                        # documents, only less than or equal 30
           r=round(len(tdoc)*0.95,3)
           
           # a raw word we need a large r
        else: 
           r=round(len(tdoc)*0.35,3)
           # a formaer word we need a small r
           
        TopQ=sorted(tdoc,key=lambda key: tdoc[key])
        
        TopResult=self.getTop(TopQ,r)
                                 
        tdoc.clear()
        
        # get the new qdoc.
        
        for value in qlist:
            for key in doc:
                temp200=key.split("[")
                term=temp200[0]
                term=term.strip(string.punctuation)
                # delete the ending punctuation
                if str(value)==term:
                    
                    p=0
                    while p<len(doc[key]):
                        doc_id=doc[key][p][0]
                        wtd=float(doc[key][p][1])
                        for values in TopResult:
                            if values==doc_id:
                                tdoc[doc_id]=wtd
                                break                        
                        p=p+1
        
        #print("after tdoc:",len(tdoc))

        qdoc,tdoc=self.find_unit_Vector(qdoc,tdoc)
          
        result=self.cos(qdoc,tdoc,k)
             
    
        top="the Inexact Top "+str(k)+" query result for the "+\
               query_terms+" is below: (about the champion)\n\n"
        
        IneCend=time.time()
        late="inexact_query about champion use "+\
                str(IneCend-IneCstart)+" seconds \n\n"
                
        self.printTo(top,late,result)
        print('inexact_query champion use %s seconds'%(IneCend-IneCstart))
        
   
    def inexact_query_elimination(self,query_terms,k):
        IneEstart=time.time()       
        doc=self.docwidf
        qlist=query_terms.split()
        #qdoc={}  first store tf-idf vlue about query
                # final store the unit vector for query        
        #tdoc={}  first store tf-idf vlue about document
                # final store the unit vector for document
       
        qdoc,tdoc=self.find_idf_To_Vector(qlist,doc,"idf")
        
        TopQ=sorted(qdoc, key=lambda key: qdoc[key])
        ## above a function sort the map according to the value
        ## result is a list about the key increasing order
        
        limit=round(len(TopQ)/2,3)
        # limit is the half thequeries term according to the
        # sorted tf-idf dreasing.
        TopQresult=self.getTop(TopQ,limit)
        
        qdoc.clear()
        
        ## get the new value about qdoc after limit.
        for values in TopQresult:          
            for key in doc:
                temp201=key.split("[")
                term=temp201[0]
                term=term.strip(string.punctuation)
                # delete the ending punctuation
                if str(values)==term:
                    #print(value)
                    temp=key.split("[")
                    value1=temp[1]
                    idf=float(value1)
                    tf_idfq=idf*1 # the value accur in query only once
                    qdoc[values]=tf_idfq
         
        qdoc,tdoc=self.find_unit_Vector(qdoc,tdoc) 
            
        result=self.cos(qdoc,tdoc,k)
    
        top="the Inexact Top "+str(k)+" query result for the "+\
               query_terms+" is below: (about the elimination)\n\n"
        
        IneEend=time.time()
        late="inexact_query about Elimination use "+\
                str(IneEend-IneEstart)+" seconds \n\n"
        
        self.printTo(top,late,result)
             
        print('inexact_query elimination use %s seconds'%(IneEend-IneEstart))

    
    def inexact_query_cluster_prunning(self,query_terms,k):
        IneCPstart=time.time()
        docW=self.docWhole
        docu=self.doc
        doc=self.docwidf
        qlist=query_terms.split()
        tdoc={}
        qdoc={}
        leader=[0]
        # restore the doc_id of each leader         

        i=random.randint(1,len(docu))
        # i is random number from 1 to len(docu)
        # at here it will be 1-423
        num=int(math.sqrt(len(docu)))
        # num is the number of the leader 
        # first we random choose the num leader
    
        for j in range(num): 
   
            for v in leader:   
               if v!=i:
                   if v==0:                 
                       leader.clear() 
                       leader.append(str(i))
                   else: 
                     
                       leader.append(str(i))
   
               break
            i=random.randint(1,len(docu))
        scoredic={}
        
        for values in leader:           
           for value in qlist:
              for key in doc:
                temp200=key.split("[")
                term=temp200[0]
                term=term.strip(string.punctuation)
                # delete the ending punctuation
                if str(value)==term:
                    temp=key.split("[")
                    value66=temp[1]
                    idf=float(value66)
                    tf_idfq=idf*1 # the value accur in query only once
                    qdoc[value]=tf_idfq
                    p=0
                    while p<len(doc[key]):
                        doc_id=doc[key][p][0]
                        if values==doc_id:
                                #doc_id=doc[key][p][0]
                                value1=float(doc[key][p][1])
                                tf_idft=idf*value1
                                tdoc[doc_id]=tf_idft 
                        p=p+1         
           qdoc,tdoc=self.find_unit_Vector(qdoc,tdoc)   
           score=0
           for d in tdoc:
               for q in qdoc:
                  score=score+qdoc[q]*tdoc[d] 
                  score=round(score,3) 
           scoredic[values]=score  
     
        
        Top=sorted(scoredic, key=lambda key: scoredic[key])  
       
        result=self.getTop(Top,num)
        
        #print(result[0])
        temp=docW[int(result[0])]+query_terms
        #self.exact_query(temp,10)
        qlist1=temp.split()
        
        qdoc,tdoc=self.find_idf_To_Vector(qlist1,doc,"idf")
        
        qdoc,tdoc=self.find_unit_Vector(qdoc,tdoc)
                                   
        finalresult=self.cos(qdoc,tdoc,k)
        
        idex=0
        
        # if the result of the first leader is not lager than 10
        # it will do the next find to their follows until
        # the final result is equal to k,this is 10. 
        while len(finalresult)<k:
               temp=docW[int(result[index+1])]+query_terms
               
               qlist2=temp.split()
              
               qdoc,tdoc=self.find_idf_To_Vector(qlist2,doc,"idf")
        
               qdoc,tdoc=self.find_unit_Vector(qdoc,tdoc)
                                   
               temp=self.cos(qdoc,tdoc,k-len(finalresult))
               for val in temp:
                   result.append(val)
               idex=idex+1            

        top="the Inexact Top "+str(k)+" query result for the "+\
               query_terms+\
               " is below: (about the query_cluster_prunning)\n\n"
            
        IneCPend=time.time()
    
        late="exact_query use "+str(IneCPend-IneCPstart)+" seconds \n\n"
        self.printTo(top,late,finalresult)
        #IneCPend=time.time()       
        print('inexact_query c_p use %s seconds'%(IneCPend-IneCPstart))



     
    
    def print_dict(self): 
        
        pstart=time.time()
        pdo=self.docwidf
        pdo=collections.OrderedDict \
         (sorted(pdo.items(),key=lambda d:d[0]))  
        pdpath=self.path
        pdpath=pdpath+"\Output.txt"
        f3=open(pdpath,"a")
        temp="Terms and posting list in the index is below:\n"       
        f3.write(temp)
        temp100=""
        for key in pdo:
             temp100=key
             p=0
             while p<len(pdo[key]):
                                 
                   if p!=len(pdo[key])-1:
                        temp100=temp100+"("+pdo[key][p][0]+","+\
                        pdo[key][p][1]+",["+\
                        pdo[key][p][2]+"]),"
                   else: 
                       temp100=temp100+"("+pdo[key][p][0]+","+\
                       pdo[key][p][1]+",["+\
                       pdo[key][p][2]+"])]\n"
                   p=p+1 
                                 
             f3.write(temp100)
             temp100=""
       
        f3.close()   
        pend=time.time()
        print('print_dict use %s seconds'%(pend-pstart))
        
    def print_doc_list(self):
        
        pdlstart=time.time()
        pdlpath=self.path  
        pdlpath=pdlpath+"\Output.txt"
        docu=self.doc
        f=open(pdlpath,"a")
        ptemp="\nThe documents and their document id is below:\n"
        for key in docu:
             ptemp=ptemp+"Doc ID: "+str(key)+" ==> "+docu[key]+"\n"
             f.write(ptemp)
             ptemp=""
        f.close()     
        pdlend=time.time()
        print('print_dict_list use %s seconds'%(pdlend-pdlstart))
      
   
      

def main():      
      path=os.getcwd()# find the directory of the 'index.py'
      ind=index(path)
      ind.buildIndex() 
    
      querylist=["there are very happy day for this meeting",\
                 "I feel glad to visit market with my mother",\
                 "Does she be a beautiful teacher or student",\
                 "terrible reason late for school",\
                 "it is the wonderful weather go climbing"]      
      # below the query search
      # and supposing the k=10
      for query in querylist:
          ind.exact_query(query,10)
          ind.inexact_query_elimination(query,10)
          ind.inexact_query_champion(query,10)
          ind.inexact_query_cluster_prunning(query,10)
                
      ind.print_dict()      
      ind.print_doc_list()
            
main()


    
        
        
    

#python 3.7
"""

@author: hailong
"""

import re
import os
import collections
import time


class index:
    
    def __init__(self,path):
        
        self.path=path
        self.doc={} # contain the documents and their document id
        self.document={} # contain the terms and posting list in 
                         # the index. 
        self.document_list={} 
       
    def buildIndex(self):
        
        start=time.time()
        paths=self.path+"\collection"
        files=os.listdir(paths)
        # above method is use to scan the context of this directory.
        doc=self.doc
        document=self.document
        doc_id=1
        document_list=self.document_list
        count=0 # this is used to record the location in the text. 
        for file in files:
            doc[doc_id]=file         
            road=paths+"\\"+file
            # this is the path to find each text.
            f=open(road,"r")
            road=paths
            whole=""
            for line in f.readlines():
                  line=line.lower()                  
                  whole=whole+line
                  word=line.split()
                  for w1 in word:
                      count=count+1
                      match=re.search("[a-z][a-z'.]*[a-z]?",w1)
                     # basic tokenization. remove all punctuations
                     # between the two words, and remove numerals.
                      if match!=None: 
                            sigword=match.group()
                            if document_list.__contains__(sigword):
                               temp=document_list[sigword] 
                               temp1=document[sigword]                             
                               if str(doc_id) not in temp:
                                   temp=temp+","+str(doc_id)
                                   document_list[sigword]=temp
                                   
                               if ")" not in temp1:                                    
                                   temp1=temp1+","+str(count)
                                   document[sigword]=temp1
                               else:
                                   match1=re.search("[0-9]",\
                                         temp1[len(temp1)-1])
                                   if match1==None:
                                         temp1=temp1+",("+str(doc_id)\
                                         +",["+str(count)
                                         document[sigword]=temp1
                                   else:
                                         temp1=temp1+","+str(count)
                                         document[sigword]=temp1
                            else:
                                   document_list[sigword]=str(doc_id)
                                   temp2="[("+str(doc_id)\
                                        +",["+str(count)
                                   document[sigword]=temp2      
                  
            for dkey in document:
                    temp6=document[dkey]
                    match6=re.search("[0-9]",\
                         temp6[len(temp6)-1])
                    if dkey in whole:
                         if match6!=None:
                            temp3=document[dkey]
                            temp3=temp3+"])"
                            document[dkey]=temp3
            doc_id=doc_id+1 
            count=0
            f.close()
        
        for dokey in document:
            temp5=document[dokey]
            temp5=temp5+"]"
            document[dokey]=temp5
         
        document_list=collections.OrderedDict \
         (sorted(document_list.items(),key=lambda d:d[0])) 
          
        #print(len(document_list))
        #print(len(document))    
        
        end=time.time()       
        bpath=self.path
        bpath=bpath+"\Output.txt"
        bf=open(bpath,"w")
        bftemp="Index built in "+str(end-start)+" seconds \n\n"
        bf.write(bftemp)
        bf.close()
        print('Index built in %s seconds'%(end-start))
        
    
    def and_query(self,query_terms):
        
        qstart=time.time()
        qpath=self.path
        temp=set(query_terms)# remove duplicate element 
        qry=list(temp)     # recovery to the list in order to 
                           # query easily.  
        doculist=self.document_list
        qdoc=self.doc
        wholeresult=""
        for i in range (len(qry)):           
           if doculist.get(qry[i])==None:
                wholeresult=""          
           else:    
               if i==len(qry)-1:
                   wholeresult=wholeresult+doculist[qry[i]]
               else:
                   wholeresult=wholeresult+doculist[qry[i]]+"," 
                
        total=len(qry) # record the number of word in the list.  
        qpath=qpath+"\Output.txt" 
        qf=open(qpath,"a")           
        qwrite="Results for the Query: "
        for j in range(len(qry)):
              if j==len(qry)-1:
                  qwrite=qwrite+qry[j]+"\n"
              else:
                  qwrite=qwrite+qry[j]+" AND "        
        qf.write(qwrite) 
        if wholeresult=="":
            qf.write("All words are not find in the document\n")
        else:   
            arrayresult=wholeresult.split(",")
            tempdic={}
            result=[]
            finalresult=[]
            i=0
            while i<len(arrayresult):
                 context=arrayresult[i]
                 if tempdic.get(context)==None:
                      tempdic[context]=1
                 else:
                      count=int(tempdic[context])
                      count=count+1
                      tempdic[context]=str(count)
                 i=i+1    
            for k in tempdic:
                 if int(tempdic[k])==total:
                      result.append(k)
                      
            # below is means the result is not empty.  
            if result:
                 for qre in result:
                      for qkey in qdoc:
                          qtemp=int(qre)       
                          if qtemp==qkey:
                             finalresult.append(qdoc[qkey])
                 qwrite="Total Docs retrieved: " \
                           +str(len(finalresult))+"\n"
                 qf.write(qwrite)              
                 qwrite=""
                 for qfr in range(len(finalresult)):              
                       qwrite=qwrite+finalresult[qfr]+"\n"
                 qf.write(qwrite)
                       
            # below is means the result is empty.            
            else:
                 qf.write("AND operater of word is not find in document\n")
                  
        qend=time.time()
        qwrite="Retrieved in "+str(qend-qstart)+" seconds \n\n"       
        qf.write(qwrite)
        qf.close()
        
        print('Retrieved in %s seconds'%(qend-qstart)) 
        
    
    def print_dict(self): 
        
        pstart=time.time()
        pddocument=self.document
        pddocument=collections.OrderedDict \
         (sorted(pddocument.items(),key=lambda d:d[0]))  
        pdpath=self.path
        pdpath=pdpath+"\Output.txt"
        f3=open(pdpath,"a")
        temp="\nTerms and posting list in the index is below:\n"
        for key1 in pddocument:
           temp=temp+key1+":"+pddocument[key1]+"\n"
           f3.write(temp)
           temp=""
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
      
      # below are five datas to text the and_query. 
      
      querylist=[['with','without','yemen'],\
                 ['with','without','yemen','yemeni'],\
                 ['zoo','zoom'],\
                 ['with','you','a','able','key'],\
                 ['kill','kind']]
      
      for query in querylist:
          ind.and_query(query)
      
      ind.print_dict()      
      ind.print_doc_list()
      
    
    
main()


    
        
        
    

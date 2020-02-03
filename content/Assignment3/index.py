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
from collections import defaultdict

class index:
    
    def __init__(self,path):
        
        self.path=path
        self.doc={} # contain the documents and their document id
        self.document={} # contain the terms and posting list in the index. 
        self.doc_length=[] # contains store document lengths 
                           #( for cosine score calculation)
        self.stop=[] # contains all the stop word.  
        self.Iter={} # contains the iteration for the rocchio algorithm
        self.inner_mark={1:"first",2:"second",3:"third"}
                     # it is the mark for the query, easy to read. 
                     
        #self.inner_num={1:8,2:15,3:9} # contains the number of relevant 
                          # document of the first query 
                                       
        self.num=defaultdict(float) 
        self.num_pseudo=defaultdict(float)                            
       
    def buildIndex(self):
        
        start=time.time()
        paths=self.path+"\\time"
        stop=self.stop
    #    files=os.listdir(paths)
        # above method is use to scan the context of this directory.
        
        # get all stop word
        stop_road=paths+"\\stp.txt"
        stop_f=open(stop_road,"r")
        for stop_line in stop_f.readlines():
            if stop_line != "\n":
               stop_line=stop_line.lower() 
               stop_word=stop_line.split() 
               stop.append(stop_word[0])               
        
        # start to token 
        stop_f.close()
        doc=self.doc
        doc_id=0
        count=0
        road=paths+"\\time.txt"
        document=self.document
        list1=[]
        f=open(road,"r")        
        #whole=""        
        for line in f.readlines():

            words=line.split()        
            # below this line is the title of the text
            if "*TEXT" in line:
               self.doc_length.append(0) 
               doc_id=doc_id+1
               count=0
               doc_name="TEXT "+words[1]+".txt"
               doc[doc_id]=doc_name
               
               #print("doc_id is ",doc_id)
                
            # below is context of above id.
            else:    
               line=line.lower() # get every word to the small letter.
               words=line.split()
               for word in words:
                   count=count+1
                   #match=re.search("[a-z][a-z'.]*[a-z]?",word)
                   match=re.search("[a-z][a-z-]+[a-z]",word)
                   pos=""
                     # above basic tokenization. remove all punctuations
                     # between the two words, and remove numerals.
                     # below read the whole context except the 
                     # stop word and the unmathched words. 
                   if match!=None and match.group() not in stop:     
                            sigword=match.group() 
                        #if sigword not in stop:   
                       #     whole=whole+sigword                   
                            sigword=sigword+":[idf" 
                            list1.append(str(doc_id))
                            temp="wtd-"+str(doc_id)
                            list1.append(temp)
                            if  not document.__contains__(sigword):                              
                                pos=str(count)                         
                                list1.append(pos)
                                document[sigword]=[]  
                                document[sigword].append([list1[0]
                                           ,list1[1],list1[2]]) 
                                list1.clear()
                            else:                               
                                num=len(document[sigword])-1
                                flag="0"
                                for v in document[sigword]:
                                    if v[0]==str(doc_id):
                                       # print(sigword,":",v[0])
                                        temp1=document[sigword][num][2]\
                                           +","+str(count)
                                        list1.append(temp1)
                                        temp1=""
                                        document[sigword][num].clear()                                   
                                        document[sigword][num]=\
                                        [list1[0],list1[1],list1[2]]
                                        flag="1"
                                        break
                                if flag=="0":          
                                   pos=str(count)
                                   list1.append(pos)
                                   document[sigword].append([list1[0]
                                           ,list1[1],list1[2]]) 
                                list1.clear()
                                
        f.close()
        self.doc_length.append(0)
        document=self.find_wtd_idf(doc_id+1,document) 
        self.document=collections.OrderedDict \
         (sorted(document.items(),key=lambda d:d[0]))       
        #print(len(document)) 
        
        # caculation the document length.
        for tok,items in document.items():
            tok_temp=tok.split("[")
            #tok_key=tok_temp[0].strip(string.punctuation)
            idf=float(tok_temp[1])              
            for item in items:
                self.doc_length[int(item[0])]+=\
                math.pow(idf*float(item[1]),2)
                       
        for index,value in enumerate(self.doc_length):
            self.doc_length[index]=math.sqrt(value)
            
            
        end=time.time()       
        bpath=self.path
        bpath=bpath+"\Output.txt"
        bf=open(bpath,"w")
        bftemp="TF-IDF built in "+str(end-start)+" seconds \n\n"
        bf.write(bftemp)        
        bf.close()
        print('TF-IDF built in %s seconds'%(end-start))
        
    # find the idf and wtd. 
    def find_wtd_idf(self,n,document):
        tf=0 # the value of the tf for each document.
        df=0 # the vlue of the df for the term.
        idf=0 # the vlue of the idf for the term
        wtd=0 # the value of the wtd for the document.
        n=n-1
        for key in document:
            p=0
            while p<len(document[key]):
              # print(len(doc[key])) 
               docu_id=document[key][p][0] 
               pos=document[key][p][2]
               if "," in pos:
                   plist=pos.split(",")
                   tf=len(plist)                  
               else: 
                   tf=1
               wtd=1+math.log10(tf)
               document[key][p].clear()
               document[key][p]=[docu_id,str(wtd),pos]
               p=p+1 
               
        for key1 in document:               
            df=len(document[key1])
            idf=math.log10(n/df)
            change=key1.split("[")
            newkey=change[0]+"["+str(idf)
            document[newkey]=document.pop(key1)
            
        for key2 in document:
            df=len(document[key2])
            if "idf" in key2:
                change=key2.split("[")
                idf=math.log10(n/df)
                change=key2.split("[")
                newkey=change[0]+"["+str(idf)
                document[newkey]=document.pop(key2)    
        return document   
    
    
    def rocchio(self,query_terms,pos_feedback,neg_feedback,alpha,beta,gamma):    
    
        query_modify=defaultdict(float)
        rel=defaultdict(float)
        unrel=defaultdict(float)
        query_temp=defaultdict(float)
        wholeword=[]        
        #query_terms,qdoc_length=self.vector_query(query_terms)         
        document=self.document
        rel_num=len(pos_feedback)
        unrel_num=len(neg_feedback)
        
        #calculation all relevation document and unrelevation document
        for key,val in document.items():
            key_temp=key.split("[")
            newkey=key_temp[0].strip(string.punctuation)
            idf=float(key_temp[1]) 
            for qindex,qval in query_terms.items():
                if qindex==newkey: 
                   query_temp[qindex]=qval
                
                   
            for item in val:
                 for index in pos_feedback:
                     if item[0]== index:
                         rel[newkey]+=idf*float(item[1])
                         
                         wholeword.append(newkey)                         
                     else:
                        rel[newkey]+=0
                        query_temp[newkey]+=0
                 for indexs in neg_feedback:
                     if item[0]==indexs:
                         unrel[newkey]+=idf*float(item[1])
                         
                         wholeword.append(newkey)   
                    
                     else:
                         unrel[newkey]+=0
 
        # below we get the beta/|Dr| part.                 
        for item,value in rel.items():
            if rel_num==0:
                rel[item]=0
            else:    
                rel[item]=value*beta/rel_num 
        # below we get the gamma/|Dnr| part        
        for item1, value1 in unrel.items():
            if unrel==0:
                unrel[item1]=0
            else:    
                unrel[item1]=value1*gamma/unrel_num
        # below we get the alpha part
        for item2,value2 in query_temp.items():
            query_temp[item2]=value2*alpha
            
        wholeword=set(wholeword)# delete the repeat words
        
        # below get the new query by using Rocchio algorithm
        for w in wholeword:
           judge=query_temp[w]+rel[w]-unrel[w]
           if judge>0:
               query_modify[w]=judge

        query_temp.clear()
        rel.clear()
        unrel.clear()
        
        return query_modify   
        
            
                               
    def query(self,query_terms,k): 
        
        self.query_search(query_terms,k,"first")
        
                
    def query_search(self,query_terms,k,choices):    
        qstart=time.time()
        tdoc=self.document
        tdoc_length=self.doc_length  
        # below are the first iteration.
        if choices=="first":
           qdoc,qdoc_length=self.vector_query(query_terms)
           result_doc=self.cosine_score(qdoc,qdoc_length,tdoc,tdoc_length)
        # below are not the first iteration   
        else:
           q_len=0 
           for que,que_val in query_terms.items():
                q_len+=math.pow(que_val,2)            
           q_len=math.sqrt(q_len) 
           qdoc=query_terms         
           result_doc=self.cosine_score(qdoc,q_len,tdoc,tdoc_length)           
                
        count=0
        if k>len(result_doc):
            k=len(result_doc)            
        qpath=self.path  
        qpath=qpath+"\Output.txt"
        docu=self.doc
        qf=open(qpath,"a")
        if choices=="first":
           self.num["num"]+=1
           top_mark="The "+self.inner_mark[self.num["num"]]+" query is:\n"
           qf.write(top_mark)
           top_mark=" "
           top="Query to search: "+query_terms+" "
           top+="Number of (top) results : "+str(k)+"\n"
           top+="Top "+str(k)+" result(s) for the query '"+query_terms+"' are:\n"
           top+="Doc id, Doc Name, Score\n"
        else:
           top="Top "+str(k)+" result(s) for query are\n" 
           top+="Doc id, Doc Name, Score\n"
        qf.write(top) 
        print(top,end="")
        top=""
        if result_doc or k!=0:
            while count<k:               
               output="" 
               for doc_key, doc_value in docu.items():
                      key=result_doc[count][0]
                      value=str(result_doc[count][1])
                      if  key==str(doc_key):
                          output=key+", "+doc_value+", "+str(value)+"\n"
                          qf.write(output)
                          print(output,end="")
                          output=""
               count=count+1
                           
        qend=time.time()        
        late="Results found in "+str(qend-qstart)+" seconds \n\n"
        qf.write(late)      
        print('Results found in %s seconds'%(qend-qstart)) 
        
        if k==0 or result_doc==False:
            qf.write("the result is empty")
            return
        
        if choices=="first":
            self.Iter["iter"]=1
        rtop="=== Rocchio Algorithm ===\n"        
        rtop+="Iteration: "+str(self.Iter["iter"])+"\n" 
        print("===Rocchio Algorithm===")       
        print("Iteration:  ",self.Iter["iter"], end="")    
        rel=input("Enter relevant document ids separated by space:")
        pos_feedback=rel.split()
        unrel=input("Enter non relevant document ids separated by sapce:")
        neg_feedback=unrel.split()
        rtop+="Enter relevant document ids separted by space: "
        for p in pos_feedback:
            rtop+=p+" "
        rtop+="\nEnter non relevant document ids separted by space: "
        for n in neg_feedback:
            rtop+=n+" "
            
        rstart=time.time()        
        rio_result=self.rocchio(qdoc,pos_feedback,neg_feedback,1,0.75,0.15)
        rend=time.time()
        print('New query computed %s seconds'%(rend-rstart)) 
        rtop+= "\nNew query computed in "+str(rend-rstart)+" seconds\n"
        rtop+="New query terms with weights:\n"
        qf.write(rtop)
        rtop=" "        
        number=len(rio_result)
        i=0
        rtemp=""
        for ritem,rio in rio_result.items(): 
            if i==0:
               rtemp+="{'"+ritem+"' : "+str(rio)+", "               
            elif i==number-1:
               rtemp+=ritem+"' : "+str(rio)+"}\n"  
            else:       
               rtemp+="'"+ritem+"' : "+str(rio)+", "        
            i=i+1
        qf.write(rtemp)        
        rtemp=" "
        choice=input("Continue with new query (y/n): ")
        if choice=="y":
           self.Iter["iter"]+=1 
           last="\ncontinue with new query (y/n): y\n" 
           qf.write(last)
           qf.close()
           last=" "                               
           #self.query_search(rio_result,10,"others") 
           self.query_search(rio_result,k,"others")       
        else:
           last="\ncontinue with new query (y/n): n\n"
           qf.write(last)   
        qf.close()    
              
    def cosine_score(self,query,qlength,document,dlength):
        
        scores=defaultdict(float)
        dtf_idf=defaultdict(float)
        
        for word,value in query.items():
            for key,items in document.items():
                key_temp=key.split("[")
                newkey=key_temp[0].strip(string.punctuation)               
                if word==newkey:                    
                    idf=float(key_temp[1])
                    for item in items:
                        doc_id=item[0]
                        wtf=float(item[1])
                        dtf_idf[doc_id]=wtf*idf
                        scores[doc_id]+=value*dtf_idf[doc_id]
                    #break
                
        for skey in scores:
            unit=qlength*dlength[int(skey)]
            if unit==0:
                scores[skey]=0
            else:
                scores[skey]=scores[skey]/unit         
            
        # below are method to get decreasing order        
        scores=sorted(scores.items(), key=lambda x: x[1], reverse=True)                
        return scores                    
        
    # find the query vector.        
    def vector_query(self,query_terms):
        document=self.document        
        
        query_document=defaultdict(float)
        # query_document store the frequet of one 
        # word in the query
        query_length=0
        token=re.split("\W",query_terms.lower())       
        for tok in token:
            for key,item in document.items():
                key_temp=key.split("[")
                newkey=key_temp[0].strip(string.punctuation)
                if tok==newkey:
                    if tok in query_document:
                        query_document[tok]+=1
                    else:
                        query_document[tok]=1
                    break
                    
                
        #calcalate the tf-idf
        for word,num in query_document.items():
            for key1,item1 in document.items():
                key1_temp=key1.split("[")
                newkey1=key1_temp[0].strip(string.punctuation)
                if word==newkey1:
                    idf=float(key1_temp[1])
                    wtf=1+math.log10(num)
                    query_document[word]=idf*wtf
                    query_length+=math.pow((idf*wtf),2)
                    break
        
        
        query_length=math.sqrt(query_length)
                        
        return query_document,query_length
        
    def print_dict(self):         
        pstart=time.time()
        pdo=self.document        
        pdpath=self.path
        pdpath=pdpath+"\Output.txt"
        f3=open(pdpath,"a")
        temp="Terms and posting list in the index is below:\n"       
        f3.write(temp)
        output=""
        for key in pdo:
             output=key
             p=0
             while p<len(pdo[key]):
                                 
                   if p!=len(pdo[key])-1:
                        output=output+"("+pdo[key][p][0]+","+\
                        pdo[key][p][1]+",["+\
                        pdo[key][p][2]+"]),"
                   else: 
                       output=output+"("+pdo[key][p][0]+","+\
                       pdo[key][p][1]+",["+\
                       pdo[key][p][2]+"])]\n"
                   p=p+1 
                                 
             f3.write(output)
             output=""             
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
        
        
    ## below are all functions for the pseudo relevance feedback.    

    
    def pseudo_query(self,pseudo_query_terms,k):
        
        self.pseudo_query_search(pseudo_query_terms,k,"first")
        
    def psuedo_title(self):        
        psepath=self.path
        psepath+="\Pseudo_Output.txt"
        psef=open(psepath,"w")
        top="this is the result of Pseudo Relevance Feedback:\n"
        psef.write(top)
        psef.close()
       
        
    
    def pseudo_query_search(self,query_terms,k,choices):
        
        pqstart=time.time()       
        tdoc=self.document
        tdoc_length=self.doc_length  
        # below are the first iteration.
        if choices=="first":
           qdoc,qdoc_length=self.vector_query(query_terms)
           result_doc=self.cosine_score(qdoc,qdoc_length,tdoc,tdoc_length)
        # below are not the first iteration   
        else:
           q_len=0 
           for que,que_val in query_terms.items():
                q_len+=math.pow(que_val,2)            
           q_len=math.sqrt(q_len) 
           qdoc=query_terms           
           result_doc=self.cosine_score(qdoc,q_len,tdoc,tdoc_length)           
     
        count=0
        if k>len(result_doc):
            k=len(result_doc)            
        qpath=self.path  
        qpath=qpath+"\Pseudo_Output.txt"
        docu=self.doc
        qf=open(qpath,"a")
        if choices=="first":
           self.num_pseudo["num"]+=1
           top_mark="The "+self.inner_mark[self.num_pseudo["num"]]+" query is:\n"
           qf.write(top_mark)
           top_mark=" "
           top="Query to search: "+query_terms+" "
           top+="Number of (top) results : "+str(k)+"\n"
           top+="Top "+str(k)+" result(s) for the query '"+query_terms+"' are:\n"
           top+="Doc id, Doc Name, Score\n"
        else:
           top="Top "+str(k)+" result(s) for query are\n" 
           top+="Doc id, Doc Name, Score\n"
        qf.write(top) 
        print(top,end="")
        top=""
        if result_doc or k!=0:
            while count<k:               
               output="" 
               for doc_key, doc_value in docu.items():
                      key=result_doc[count][0]
                      value=str(result_doc[count][1])
                      if  key==str(doc_key):
                          output=key+", "+doc_value+", "+str(value)+"\n"
                          qf.write(output)
                          print(output,end="")
                          output=""
               count=count+1
        
        pqend=time.time()        
        late="Results found in "+str(pqend-pqstart)+" seconds \n\n"
        qf.write(late)      
        print('Results found in %s seconds'%(pqend-pqstart)) 
        
        if k==0 or result_doc==False:
            qf.write("the result is empty")
            return
        
        if choices=="first":
            self.Iter["iter"]=1
        rtop="=== Rocchio Algorithm ===\n"        
        rtop+="Iteration: "+str(self.Iter["iter"])+"\n" 
        print("===Rocchio Algorithm===")       
        print("Iteration:  ",self.Iter["iter"], end="")    
        #rel=input("Enter relevant document ids separated by space:")
        newcount=0
        neg_feedback=""
        pos_feedback=""
        # suppose the top 3 reulst are considered to be relevant.
        while newcount<k:
            result_id=result_doc[newcount][0]
            if newcount<=2:
                pos_feedback+=result_id+" "
            else:
                neg_feedback+=result_id+" "        
            newcount+=1
            
        print("\nThe relevant document ids is:",pos_feedback)
        print("The non Relevant document ids is:",neg_feedback)
        pos_feedback=pos_feedback.split()
        #unrel=input("Enter non relevant document ids separated by sapce:")
        neg_feedback=neg_feedback.split()
        rtop+="The relevant document ids is: "
        for p in pos_feedback:
            rtop+=p+" "
        rtop+="\nThe non relevant document ids is: "
        for n in neg_feedback:
            rtop+=n+" "
            
        prstart=time.time()        
        rio_result=self.rocchio(qdoc,pos_feedback,neg_feedback,1,0.75,0.15)
        prend=time.time()
        print('pseudo Relevance Feedback is %s seconds'%(prend-prstart)) 
        rtop+= "\npseudo Relevance Feedback is "+str(prend-prstart)+" seconds\n"
        rtop+="New query terms with weights:\n"
        qf.write(rtop)
        rtop=" "        
        number=len(rio_result)
        i=0
        rtemp=""
        for ritem,rio in rio_result.items(): 
            if i==0:
               rtemp+="{'"+ritem+"' : "+str(rio)+", "               
            elif i==number-1:
               rtemp+=ritem+"' : "+str(rio)+"}\n"  
            else:       
               rtemp+="'"+ritem+"' : "+str(rio)+", "        
            i=i+1
        qf.write(rtemp)        
        rtemp=" "
        choice=input("Continue with new query (y/n): ")
        if choice=="y":
           self.Iter["iter"]+=1 
           last="\ncontinue with new query (y/n): y\n" 
           qf.write(last)
           qf.close()
           last=" "                               
           #self.pseudo_query_search(rio_result,10,"others")  
           self.pseudo_query_search(rio_result,k,"others")                  
        else:
           last="\ncontinue with new query (y/n): n\n"
           qf.write(last)   
        qf.close()    
        
        
      
def main():      
      
      path=os.getcwd()# find the directory of the 'index.py'
      ind=index(path)
      ind.buildIndex() 
      
      # below we choose 3 query to run my system
      # and id is 6 39 68 seperately
      
      
      que=["CEREMONIAL SUICIDES COMMITTED BY SOME BUDDHIST MONKS IN SOUTH VIET NAM AND WHAT THEY ARE SEEKING TO GAIN BY SUCH ACTS.",\
           "COALITION GOVERNMENT TO BE FORMED IN ITALY BY THE LEFT-WING SOCIALISTS, THE REPUBLICANS, SOCIAL DEMOCRATS, AND CHRISTIAN DEMOCRATS.",\
           "INDIAN FEARS OF ANOTHER COMMUNIST CHINESE INVASION."
          ]
      
      
      que_number={1:9,2:9,3:8} # give the relevant number of each query.
                               # 1:9 means the first query have 9
                               #relevant documents.
      mark={1:"first",2:"second",3:"third"}
      
      
      # below are Relevance feedback with query.
      qnumber=0
      for q in que:
          qnumber+=1
          print("The ",mark[qnumber]," query is:")
          ind.query(q,que_number[qnumber])
      
        
      # below are used for Psedu Relevance Feedback with the same query.  
      ind.psuedo_title()
      qnumber=0
      for pq in que:
          qnumber+=1
          print("Below are result for the Pseudo Relevance Feedback\n")
          print("The ",mark[qnumber]," query is:")
          ind.pseudo_query(pq,que_number[qnumber])
                
      ind.print_dict()      
      ind.print_doc_list()
      
    
    
main()


    
        
        
    

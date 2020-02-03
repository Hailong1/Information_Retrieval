# python 3.7

import re
import os
import collections
import time
import math
from collections import defaultdict
import random

class kmeans:
    
     
    def __init__(self,path_to_collection):
        
        self.path=path_to_collection
        self.doc={} # contain the documents and their document id
        self.document={} # contain the terms and posting list in the index. 
        #self.doc_length=[] # contains store document lengths 
                           #( for cosine score calculation)
        self.stop=[] # contains all the stop word. 
        self.tf_idf={} # contain doucment vector.
    
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
                
        for line in f.readlines():

            words=line.split()        
            # below this line is the title of the text
            if "*TEXT" in line:
               #self.doc_length.append(0) 
               doc_id=doc_id+1
               count=0
               doc_name="TEXT "+words[1]+".txt"
               doc[doc_id]=doc_name
            # below is context of above id.
            else:    
               line=line.lower() # get every word to the small letter.
               words=line.split()
               for word in words:
                   count=count+1
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
        document=self.find_wtd_idf(doc_id+1,document)  
        self.document=collections.OrderedDict \
         (sorted(document.items(),key=lambda d:d[0]))         
    
        end=time.time()       
        print('TF-IDF built in %s seconds'%(end-start))
        self.title()

    # find the idf and wtd and initial the document vectors. 
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
        
        # below are initial the document vectors.
        print("generate documents vectors: ")        
        for doc_key,doc_items in self.doc.items():
            print("Finishing ",doc_key," documents")
            self.tf_idf[doc_key]=[]
            for key,items in document.items():
                key_temp=key.split("[")                   
                idf=float(key_temp[1])
                for item in items:
                    doc_id=int(item[0])
                    wtf=float(item[1])
                    if doc_key==doc_id:
                        tf_idf=idf*wtf
                        self.tf_idf[doc_key].append(tf_idf)
                        break;        
        return document  
                  
    def title(self):
        path=self.path
        path+="\Output.txt"
        title="The result is list below\n"
        f1=open(path,"w")
        f1.write(title)
        f1.close()
    
    # below are kmean algorithm.     
    def clustering(self, kvalue):     
        start=time.time()
        times=10
        average_vector={}        
        seed=random.sample(range(1,len(self.doc)),kvalue)
        count=0 # cluster number
        for s in seed:
            count+=1
            for key,item in self.tf_idf.items():
                if s==key: 
                   average_vector[count]=item  
        for t in range(times):
                 
                doc_clu={}
                for key in average_vector:
                    doc_clu[key]=[]            
                min_number={} # store the result for find the min one
                num=0                
                for out_key,out_list in self.tf_idf.items(): 
                   count=1 
                   for key,item_list in average_vector.items():
                       doc_length=len(out_list)
                       vec_length=len(item_list)
                       for j in range(abs(doc_length-vec_length)):
                           if doc_length>=vec_length:
                               item_list.append(0)
                           else:
                               out_list.append(0)
                       for k in range(len(item_list)):
                           num+=math.pow((item_list[k]-out_list[k]),2)
                       num=math.sqrt(num)
                       min_number[count]=num
                       count+=1
                   result=sorted(min_number.items(), key=lambda x: x[1], reverse=True)
                   index=result[len(result)-1][0]                   
                   doc_clu[index].append(out_key)                
                average_vector.clear()
                count1=1    
                for key,item in doc_clu.items():                    
                    temp_list=[]                        
                    for in_key,value in self.tf_idf.items():
                        for item_value in item:    
                             if in_key==item_value:                                
                                 temp_list.append(value)       
                    temp_dic=defaultdict(float)
                    vector=0                   
                    temp_length={}
                    for temp2 in range(len(temp_list)):
                        temp_length[temp2]=len(temp_list[temp2])
                    temp_result=sorted(temp_length.items(), key=lambda x: x[1], reverse=True)
                    if len(temp_list)!=0:
                        max_one=temp_result[0][1]
                    for l in temp_list:
                        num_l=max_one-len(l)
                        for w in range(num_l):
                            l.append(0)                       
                    for row in range(len(temp_list)):
                        for line in range(len(temp_list)):     
                           temp_dic[vector]+= temp_list[line][row]
                         
                        temp_dic[vector]/=len(temp_list)
                        vector+=1    
                    temp_list1=[]    
                    for key,item in temp_dic.items():    
                        temp_list1.append(item)
                    average_vector[count1]=temp_list1
                    count1+=1
                    
        end=time.time();
        date=end-start
        self.printTo(average_vector,doc_clu,kvalue,date)
  
    #below are print to the final result.
    
    def printTo(self,vector,clu,kvalue,date):        
        path=self.path
        near_dic={}
        out_count=1
        Rss_k={}
        for key_v,item_v in vector.items():          
            numRSSk=0
            count=1
            min_number={}
            for item_c in clu[key_v]:
                num=0
                for in_key,in_list in self.tf_idf.items():
                    
                    if item_c==in_key:
                        for k in range(len(item_v)):
                            num+=math.pow((in_list[k]-item_v[k]),2)                       
                min_number[count]=num
                count+=1
            if not min_number:
                min_number[0]=0
            rank=sorted(min_number.items(), key=lambda x: x[1], reverse=True)
            rank_index=rank[len(rank)-1][0]
            nestone=rank_index 
            near_dic[key_v]=nestone
            for key_m,value_m in min_number.items():
                numRSSk+=value_m
            Rss_k[out_count]=numRSSk
            out_count+=1           
        RSS=0
        print ("Below are situation for k=",kvalue)
        for outkey,outvalue in Rss_k.items():
            RSS+=outvalue
            print(outkey,": cluster RSSk=",outvalue," and the document ID",\
                  "closest to its centroid is ",near_dic[outkey])                  
        avg_RSS=RSS/len(self.doc)
        print ("The average RSS value is ",avg_RSS)
        print('Time Taken for computation is in %s seconds'%(date))
        path=path+"\Output.txt"
        f2=open(path,"a")
        out=""
        out="Below are situation for k="+str(kvalue)+"\n"
        for key,value in Rss_k.items():
            out+=str(key)+": cluster RSSk="+str(value)+" and the document ID"+\
                 "cloest to its centroid is "+str(near_dic[key])+"\n"
        out+="The average RSS value is "+str(avg_RSS)+"\n"
        out+="Time Taken for computation is in "+str(date)+" s\n"
        f2.write(out)
        f2.close()  
        
def main():            
      path=os.getcwd()# find the directory of the 'index.py'
      ind=kmeans(path)
      ind.buildIndex()
      kvalue=[i for i in range(2,5)]
      for k in kvalue:
          ind.clustering(k)
          
main()


          

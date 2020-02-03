#python 3.7
"""

@author: hailong
"""
import re
import os
import collections
import time
import numpy
import math
from collections import defaultdict


class pagerank:
    
    def __init__(self,path):
        
        self.path=path
        self.matrix=[]
        self.pi={}
    
    def pagerank(self,input_file):
        
        #function to implement pagerank algorithm
        #input_file-input file that follows the format provided in 
        #the assignment description.
        
        start=time.time()
        dic_number=defaultdict(float)
        # above is used to count the number of the outlink of one node
                        
        # below are initial the input and initial the martix.
        # and calculation which one should get 1. 
        path=self.path
        road=path+"\\"+input_file
        f=open(road,"r")
        count=0
        smooth=0
        for line in f.readlines():
            count+=1
            if count==1:
                N=int(line)
                smooth=0.15/N
                self.matrix=numpy.zeros((N,N)) 
                # above are initial the matrix
            if count>2:
                match=re.search("[0-9 ]+",line)
                if match!=None:
                    web=line.split()               
                    web[0]=int(web[0])
                    web[1]=int(web[1]) 
                    for row in range(N):
                        for column in range(N):
                            if web[0]==row and web[1]==column: 
                                 if self.matrix[row][column]==0:
                                    self.matrix[row][column]=1 
                                    dic_number[row]+=1
               
        f.close()  
        dic_number=collections.OrderedDict \
         (sorted(dic_number.items(),key=lambda d:d[0]))
         
        ## below is to implement that
        # one row do not have 1 
        # so in this line it should be valued 1/N
        one_flag=False 
        for row in range(N):
            one_flag=False
            for column in range(N):
                if self.matrix[row][column]==1:
                    one_flag=True                    
            if one_flag==False:
                for new_column in range(N):
                    self.matrix[row][new_column]=1/N
                                
       ## below is to implement that one row have at lest one 1                                     
        for row in range(N):
            for column in range(N):
                if self.matrix[row][column]==1 \
                or self.matrix[row][column]==0:
                    
                    self.matrix[row][column]/=dic_number[row]
                    self.matrix[row][column]*=0.85
                    self.matrix[row][column]+=smooth
                   
        print("\nThe matrix for ",input_file, "are: \n",self.matrix)
        # Above finishing to initial the matrix.
        # ======================================
        
        
        # below to start to calculate the pankrank.       
        vector_x={} # contain the vector for the last one 
                    # for comparision. At start it is the 
                    # initial one.                   
        for i in range(N):            
            vector_x[i]=1/N        
        
        flag=True # judge whether the vector_x is the steady value
                   # that is the vector_x not changed or not.             
        while flag:             
            temp_x=defaultdict(float)           
            number=0
            for column in range(N):   
                row=0
                for vec_key,vec_value in vector_x.items():          
                    temp_x[number]+=vec_value*self.matrix[row][column]                    
                    row+=1                     
                number+=1                  
            
            
            # below is to check the equation 
            # pi=pi*matrix, if the result is true
            # the value of flag will be False. 
            # which means that needing to stop the iteration
            # and get the finial result.
            equal_count=0            
            for idex in range(N): 
                if math.isclose(vector_x[idex],temp_x[idex]): 
                    equal_count+=1
                elif temp_x[idex]>0.999:
                    flag=False
                    self.pi=temp_x
            if equal_count==N:
               flag=False 
               self.pi=temp_x
            else:
               vector_x.clear()
               vector_x=temp_x  
        end=time.time()
        print('Pagerank algorithm is finished in %s seconds'%(end-start))
        
        # below are function to print the pageranks for top 10 pages
        self.print_Top(self.pi)
        
        # below are function to store the pageranks for all pages
        # in the output file "Output.txt",which is located as the same
        # directory as the pagerank.py          
        self.store_Whole_Value(self.pi,input_file,N)
        

    def print_Top(self,result):
       top_result=sorted(result.items(), key=lambda x: x[1], reverse=True)       
       if len(top_result)>=10:
           print("\nThe top 10 pages are: ")
           number=10
       else:
           print("\nThe total number of pages is less than 10.",end="")
           print("So the ranked whole pages are:")
           number=len(top_result)
       print("page id \t pagerank value\t")    
       for item in range(number):
           print(top_result[item][0],"\t\t",top_result[item][1])
           
       
    def store_Whole_Value(self,result,choice,N):
       store_path=self.path
       store_path+="\\Output_"+choice
       f=open(store_path,"w")
       inner_title=""
       inner_title="Output for file  "+choice
       inner_title+="\nUsing initial vector with value of 1/"+\
                     str(N)+" for each element \n"
       inner_title+="The whole page rank for "+choice+" are:\n"
       inner_title+="Page Id \t Page Rank Score\n"
       inner_title+="========================================\n"
       f.write(inner_title)
       fwrite=""
       for index,value in result.items():
           fwrite+=str(index)+"\t\t"+str(value)+"\t\n"
       f.write(fwrite)
       fwrite=""
       f.close()
       
                                               
def main():
    
   path=os.getcwd() # find the directory of the 'index.py'  
   ind=pagerank(path)

   test=["test1.txt","test2.txt",]
   
   # below are iteration for the test the algorithm
   for t in test:
       ind.pagerank(t)

   
   
   
main()   
   
          
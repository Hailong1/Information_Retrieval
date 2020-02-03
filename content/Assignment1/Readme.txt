  
  ReadMe
  
   The environment of my program is using Python3.7 and using Spyder IDE and the operation system is Windows 8
   In the program, we have the following function:
   main() function:
   It is defined for running the program.In this function, firstly, it finds the directory where the 'index.py' is located by using the os.getcwd() method. And it then calls the buildIndex() to build index. And then it gives the 5 query to test the And_query() function. Finally it calls print_dict() and print_doc_list() to export the terms and posting list, the documents and their document id separately.And it exports the time for building the index to the 'Output.txt' that will be located in the same directory as the 'index.py'.

   buildIndex() function:
   In this function,it reads documents from collection,tokenize and build the index with tokens. And we need to put 'collection' file in the same directory as the 'index.py'. And the index contains positional information of the terms in the document. We also use unique document IDs.

   print_dict() function:
   This function print the terms and posting list in the index into the 'Output.txt'.

   print_doc_list() function:
   This function print the documents and their document id into the 'Output.txt'.

   and_query() function:
   This function identifies relevant docs using the index and exports the query result and the time for processing the query into the 'Output.txt'.The merge algorithm for processing AND Bollean queries as the following:
   1. we get list from query_terms and remove duplicate element and     
      record the number of words of the lists.  
   2. we scan every posting list of above words to put corresponding 
      document id into a list 
   3. combing all above document id list into one list. 
   4. Scan the combined list and count the number of every                 
      elements that appear in the list. 
   5. if the total number of the element in the above list equals to  
      number of words of the list that we get from the query_terms,
      those element will be the result of the query. (since each 
      element will appear in the document id list that is produced by 
      step 3 only once, if above condition  is true, it means the             
      element will appear in each dument id list that is produced by   
      step 3 ) .

  Finally, the program will generate a 'Output.txt' that is contained context that is mentioned above. And in this text document. If the result of two or more AND operator is empty, it will export 'AND operater of word is not find in document'. If the whole word about query are not find in the posting list in the index. it will export 'All words are not find in the document'. Remain situation, it will export the correct result. 
  
     
   

            

    
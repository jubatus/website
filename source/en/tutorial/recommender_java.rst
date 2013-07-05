Java
==================

Here we explain the sample program of Recommender in Java. 

--------------------------------
Source_code
--------------------------------

In this sample program, we will explain 1) how to configure the learning-algorithms that used by Jubatus, with the example file 'ml.json'; 2) how to train the model by 'Update.java' with the training data in 'u.data' file, and how to recommend with 'Analyze.java'. Here are the source codes of 'ml.json', 'Update.java' and 'Analyze.java'.


**ml.json**

.. code-block:: python
  
 01: { 
 02:   "converter" : { 
 03:     "string_filter_types": {}, 
 04:     "string_filter_rules":[], 
 05:     "num_filter_types": {}, 
 06:     "num_filter_rules": [], 
 07:     "string_types": {}, 
 08:     "string_rules":[ 
 09:             {"key" : "*", "type" : "str", "sample_weight":"bin", "global_weight" : "bin"}  
 10:                    ], 
 11:     "num_types": {}, 
 12:     "num_rules": [ 
 13:       {"key" : "*", "type" : "num"} 
 14:                  ] 
 15:   }, 
 16:   "parameter" : { 
 17:     "bit_num" : 128 
 18:   }, 
 19:   "method": "lsh" 
 20: } 

**Update.java**

.. code-block:: java

 01:  package us.jubat.example.ml;
 02: 
 03:  import java.io.BufferedReader;
 04:  import java.io.File;
 05:  import java.io.FileNotFoundException;
 06:  import java.io.FileReader;
 07:  import java.io.IOException;
 08:  import java.util.ArrayList;
 09:  import java.util.Arrays;
 10:  import java.util.List;
 11:  import us.jubat.recommender.RecommenderClient;
 12:  import us.jubat.recommender.Datum;
 13:  import us.jubat.recommender.TupleStringDouble;
 14:  import us.jubat.recommender.TupleStringString; 

 15:  public class Update {
 16:   public static final String HOST = "127.0.0.1";
 17:   public static final int PORT = 9199;
 18:   public static final String NAME = "ML";
 19:   public static final String Data_PATH = "../dat/ml-100k/u.data";
 20: 
 21:   public void start() throws Exception {
 22:           // 1. Connect to Jubatus Server
 23:           RecommenderClient client = new RecommenderClient(HOST, PORT, 5);
 24: 
 25:           // 2. Prepare training data
 26: 
 27:           try{
 28:                   File csv = new File(Data_PATH); // read data file
 29:  
 30:                   BufferedReader br = new BufferedReader(new FileReader(csv));
 31: 
 32:                   String line = "";
 33: 
 34:                   // read the file line by line til the end
 35:                   while ((line = br.readLine()) != null) {
 36: 
 37: 
 38:                        Datum datum = new Datum();
 39:                        datum.string_values = new ArrayList<TupleStringString>();
 40:                        datum.num_values = new ArrayList<TupleStringDouble>();
 41:                        // split the line for items
 42:                        String[] strAry = line.split("\t");
 43:   
 44:                        try{
 45:                            TupleStringDouble data = new TupleStringDouble();
 46:                            data.first = strAry[1];
 47:                            data.second = Double.parseDouble(strAry[2]);
 48:                            datum.num_values.add(data);
 49: 
 50:                        }catch(NumberFormatException e){
 51:                        }
 52: 
 53:                        //3. training the model
 54:                        client.update_row(NAME, strAry[0], datum);
 55:                   }
 56:                   br.close();
 57: 
 58:           } catch (FileNotFoundException e) {
 59:                 // capture exception when creating file object
 60:                 e.printStackTrace();
 61:           } catch (IOException e) {
 62:                 // capture exception when close BufferedReader object
 63:                 e.printStackTrace();
 64:        }
 65:        return;
 66:   }
 67:
 68:   // Main method
 69:   public static void main(String[] args) throws Exception {
 70:        new Update().start();
 71:        System.exit(0);
 72:   }
 73: }


**Analyze.java**

.. code-block:: java

 01:  package us.jubat.example.ml;
 02:
 03:  import java.io.BufferedReader;
 04:  import java.io.File;
 05:  import java.io.FileNotFoundException;
 06:  import java.io.FileReader;
 07:  import java.io.IOException;
 08:  import java.util.ArrayList;
 09:  import java.util.List;
 10:  
 11:  
 12:  import us.jubat.recommender.RecommenderClient;
 13:  import us.jubat.recommender.TupleStringFloat; 
 14: 
 15:  public class Analyze {
 16:    public static final String HOST = "127.0.0.1";
 17:    public static final int PORT = 9199;
 18:    public static final String NAME = "ML";
 19: 
 20:   
 21: 
 22:    public void start() throws Exception {
 23:        // 1. Connect to Jubatus Server
 24:        RecommenderClient client = new RecommenderClient(HOST, PORT, 5);
 25: 
 26:        // 2. Get the recommended results for every user
 27:        List<TupleStringFloat> rec = new ArrayList<TupleStringFloat>(); 
 28:   
 29:        for (int i=0; i<=100000; i++) {
 30:          rec = client.similar_row_from_id("movie_len", Integer.toString(i), 10);                         
 31:        //3. Output result
 32:          System.out.print("audience " + Integer.toString(i) + " is similar to : " );
 33:          for (int j=0; j<10; j++){
 34:              System.out.print(rec.get(j).first + " ");
 35:          }
 36:          System.out.println();
 37:        }
 38:        return;
 39:    }
 40: 
 41:    // Main method
 42:    public static void main(String[] args) throws Exception {
 43:        new Analyze().start();
 44:        System.exit(0);
 45:    }
 46: }



--------------------------------
Explanation
--------------------------------

**ml.json**

The configuration information is given by the JSON unit. Here is the meaning of each JSON filed.

* method

 Specify the algorithm used in classification. 
 This time, we specify it with "lsh", because we want to use Locality Sensitive Hashing.
 Besides "lsh", we also support "minhash", "inverted_index" and "euclid_lsh".

* converter

 Specify the configurations in feature converter.
 In this example, we will set the "num_rules".
 
 "num_rules" are used to specify the extraction rules of numercial features.
 "key" is "*", it means all the "key" are taken into consideration, "type" is "num", it means the number(value) specified will be directly used as the input for training the model. 
 For example, if the "movie-ranking = 3", use 3 as the input.

 "string_rules" are used to specify the extraction rules of string features.
 Because string features are not used, we don't provide the "String_rules" explaination here. 
  
* parameter

 Specify the parameters to be passed to the algorithm.
 The method specified here is "lsh", so parameter 'bit_num' is required. It means the bits number in hash value. The bigger it is, the higher accuracy and more memory comsumption there will be.


We explain the learning and recommendation processes in this example.

 To write the Client program for Recommender, we can use the RecommenderClient class defined in 'us.jubat.recommender'. There are two methods used in this program. The 'update_row' method for learning process, and the 'analyze' method for recommendation with the data learnt.
 

**Update.java**

 1. Connect to Jubatus Server

  Connect to Jubatus Server (Row 23)
  Setting the IP addr., RPC port of Jubatus Server, and the connection waiting time.


 2. Prepare the training data

  Prepare the Datum for model training (Row 35-51). Basically, the training datum contains two parts, string_values & num_values, each of StringString type & StringDouble type, respectively. Because in this sample, only the "movie-id"(String type) & "movie-ranking"(Integer type) are used for training the model, only the num_values part is filled with the data while leaving the string_values "null". 

  Here is the detailed process for making the training data in this sample.
  
  First, read the source file (u.data) of the training data.
  Here, BuffererdReader() is used to read the items in source file line by line (Row 35).
  Split the data in each line by '\t' (Row 42). And use 'movie-id' & 'movie-ranking' value to fill the datum.num_values (Row 45-48). Leaving the datum.string_values 'null', because no stringstring type data is used as input.
  
 
 3. Model Training (update learning model

  Input the training data generated in step.2 into the update_row() method (Row 54).
  The first parameter in update_row() is the unique name for task identification in Zookeeper.
  (use null charactor "" for the stand-alone mode)
  The second parameter specifies the unique ID for each audience. In this example, it is the "id" of each audience.
  The third parameter is the Datum for each audience, that generated in Step 2.
  Now, the Datum of one audience has been learnt. By looping the Steps 2 & 3 above (Row 35), all the audiences' data in the u.data file will be learnt.

**Analyze.java**

 1. Connect to Jubatus Server

  As the same as Update.java.
  
 2. Get the recommended results for every user

  In step 2, we firstly declare a result list 'rec', to store the returned list from Jubatus server at line 27.  In this sample, the returned value contains the <"audience-id", "similarity-degree">, so the 'rec' is in StringFloat type. Then, we try to get the recommended results for the whole audiences (line 29), whose ids are in {1, 100000}, one by one.  The 1st parameter in client's method "similar_row_from_id()"  is used as an identity for the model in Jubatus server, which could in any terms; the 2nd parameter is the id of current audience, whose similar audiences you are looking for; the 3rd parameter is the number of most liked audience you want to be returned. In this example, we want to get the most liked 10 people returned in result.

 3. Output result

  In step 3, we print out the returned data in 'rec'. For simplicity, the first part in each 'rec', which is the similar audience's id, is print out (line 34).
Note that, among teh returned 10 'id's, the top-1 is the input audiences itself. Because it has the highest similarity to herself.
  

------------------------------------
Run the sample program
------------------------------------

**[At Jubatus Server]**
 
 start "jubarecommender" process.

::

 $ jubarecommender --configpath ml.json


**[At Jubatus Client]**

 Get the required package and Java client ready.
 
**[Result]**

::

 …(omitted)
 …
 audience 436 is similar to : 436 42 654 472 588 268 899 606 586 551 
 audience 437 is similar to : 437 194 10 711 846 527 474 189 18 90 
 audience 438 is similar to : 438 540 580 768 231 141 891 839 779 730 
 audience 439 is similar to : 439 697 399 99 917 689 507 291 825 742 
 audience 440 is similar to : 440 898 136 894 414 829 74 724 574 489 
 audience 441 is similar to : 441 935 742 612 602 190 17 879 678 277 
 audience 442 is similar to : 442 268 267 758 586 56 5 497 457 399 
 …
 …(omitted)

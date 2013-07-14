Ruby
==================

Here we explain the sample program of Recommender in Ruby.

--------------------------------
Source_code
--------------------------------

In this sample program, we will explain 1) how to configure the learning-algorithms that used by Jubatus, with the example file 'ml.json'; 2) how to train the model by 'Update.rb' with the training data in 'u.data' file, and how to recommend with 'Analyze.rb'. Here are the source codes of 'ml.json', 'Update.rb' and 'Analyze.rb'.


**ml.json**

.. code-block:: ruby

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


**Update.rb**

.. code-block:: ruby

 01: require 'jubatus/recommender/client'

 02: NAME = "recommender_ml"

 03: recommender = Jubatus::Recommender::Client::Recommender.new "127.0.0.1", 9199
 04: n = 0
 05: File.open("./dat/ml-100k/u.data", "r").each{|line|
 06:   userid, movieid, rating, mtime = line.split(' ')
 07:   datum = Jubatus::Recommender::Datum.new [],[[movieid.to_s, rating.to_f]]
 08:   if (n % 1000 == 0)
 09:     p n
 10:   end
 11:   recommender.update_row(NAME, userid, datum)
 12:   n = n + 1
 13: }


**Analyze.rb**

.. code-block:: ruby

 01: require "jubatus/recommender/client"
 02: require "jubatus/recommender/types"
 03: require "pp"

 04: recommender = Jubatus::Recommender::Client::Recommender.new "127.0.0.1", 9199

 05: Array.new(943){|index| "#{index}"}.each{|n|
 06:   sr = recommender.similar_row_from_id("movie_len", n.to_s, 10)
 07:   print "user#{n} is similar to "
 08:   sr.each{|user_tuple|
 09:     print(" user#{user_tuple[0]} score:#{user_tuple[1]}  ")
 10:   }
 11:   puts ""
 12: }


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
 
We explain the learning and recommendation processes in this example.


 To write the Client program for Recommender, we can use the RecommenderClient class defined in 'us.jubat.recommender'. There are two methods used in this program. The 'update_row' method for learning process, and the 'analyze' method for recommendation with the data learnt.
 

 
**Update.rb**

 1. Connect to Jubatus Server

  Connect to Jubatus Server (Line 3)
  Setting the IP addr., RPC port of Jubatus Server.

 2. Prepare the training data

  Prepare the Datum for model training (Line 6). Basically, the training datum contains two parts, string_values & num_values, each of StringString type & StringDouble type, respectively. Because in this sample, only the "movie-id"(String type) & "movie-ranking"(Integer type) are used for training the model, only the num_values part is filled with the data while leaving the string_values "null". 

  Here is the detailed process for making the training data in this sample.
  
  First, read the source file (u.data) of the training data (Line 5).
  Split the data in each line by '\t' (Line 6). Get the 'movie-id' & 'movie-ranking' value, and fill them into the training datum (Line 7). Leaving the datum's string-string_value as 'null', because no string-string type data is used as input.

 3. Model Training (update learning model

  Input the training data generated in step.2 into the update_row() method (Line 7).
  The first parameter in update_row() is the unique name for task identification in Zookeeper.
  (use null charactor "" for the stand-alone mode)
  The second parameter specifies the unique ID for each players. In this example, the "name" of each player is used as the ID.
  The third parameter is the Datum for each player, that generated in Step 2.
  Now, the Datum of one audience has been learnt. By looping the Steps 2 & 3 above, all the audiences' data in the CSV file will be learnt.



**Analyze.rb**

 1. Connect to Jubatus Server

  As the same as Update.rb.
  
 2. Get the recommended results for every user

  In step 2, we get the returned list from Jubatus server at line 6. The returned value contains the <"audience-id", "similarity-degree">. We try to get the recommended results for the audiences (line 5), whose ids are in {0, 943}, one by one.  The 1st parameter in client's method "similar_row_from_id()"  is used as an identity for the model in Jubatus server, which could in any terms; the 2nd parameter is the id of current audience, whose similar audiences you are looking for; the 3rd parameter is the number of most liked audience you want to be returned. In this example, we want to get the most liked 10 people returned in result.

 3. Output result

  In step 3, we print out the returned data in 'sr'. Note that, among teh returned 10 'id's, the top-1 is the input audiences itself. Because it has the highest similarity to herself.

------------------------------------
Run the sample program
------------------------------------

**[At Jubatus Server]**
 
 start "jubarecommender" process.

::

 $ jubarecommender --configpath ml.json

**[At Jubatus Client]**

 Run the commands below.

::

 $ ruby update.rb
 $ ruby analyze.rb

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


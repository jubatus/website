Recommender
===================

In this sample program, we will introduce how to use the Recommender function 'jubarecommender' through the Jubatus Client.

By using Recommender, we can recommend the similar data or data with the similar attribute. This function is useful for the EC site products recommendation or the linked ads recommendation in search site.

-----------------------------------
Abstract of sample program
-----------------------------------

In this sample, I will use a sample program, named 'movielens', to study 100,000 audience's opinions over about 1,000 movies, and then recommend similar audiences for each of them.

To training the model, please download the `audience opinions data <http://www.grouplens.org/system/files/ml-100k.zip>`_ at first. `unzip ml-100k.zip` to extract for the `u.data` file which will be used in this sample program. It contains the values of <'audience-id';  'movie-id';  'movie-ranking';  'movie-length'>, which means the audience<'audience-id'> ranked the movie<'movie-id'> at 'movie-ranking' in his/her subjective opinion, the 'movie-length' is an objective attribute of movie<'movie-id'>. 
These data will be used to training the recommendation model at Jubatus server.

To get the recommended similar audiences of audience<'x'>, we will send its audience-id 'x' to Jubatus server through our Jubatus client method. And then, the most similar audiences list is returned as the recommendation result. 

--------------------------------
Processing flow 
--------------------------------

Main flow of using Jubatus Client

* Upadate

 1. Connection settings to Jubatus Server

  Setting the HOST, RPC port of Jubatus Server

 2. Prepare the training data

  Get all the audience data from the u.data file.

 3. Data training (update the model)

  Get the audience's data line by line, and send to Jubatus server by the Jubatus client method update_row() to train the model.

* Analyze

 1. Connection settings to Jubatus Server

  Setting the HOST, RPC port of Jubatus Server

 2. Get the recommended results for every user

  Get similar audiences of audience-'x' from its recommendation results, by using the client method similar_row_from_id().

 3. Output the result

  Output the returned results from similar_row_from_id().

--------------------------------
Sample program
--------------------------------

.. toctree::
   :maxdepth: 2

   recommender_python
   recommender_ruby
   recommender_java

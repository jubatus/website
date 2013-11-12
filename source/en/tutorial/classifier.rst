Classifier
=================

In this section, we will introduce how to use ``jubaclassifier`` through the Jubatus Client.

Classifier is the function to classify given data. For example, You can use Classifier to detection of spam mail.

-------------------------------------
Overview
-------------------------------------

The sample program is `gender <https://github.com/jubatus/jubatus-example/tree/master/gender>`_ . This program will classify data into male or female through the features of hair style, height and clothes.

As a first step, update model in ``jubaclassifier`` using the training data.

The training data is a pair of class(male or female) and features(hair style, height, clothes). You will prepare some training data and make ``jubaclassifier`` learn those data.

Next, analyze the test data using model in ``jubaclassifier`` .

You will prepare features as a test data, ``jubaclassifier`` will classifiy this into male or female using model.

For example, you give the feature data as following, ``jubaclassifier`` will return "female".

::

  "hair" is "long"
  "top" is "shirt"
  "bottom" is "skirt"
  "height" is 1.50


--------------------------------
Scenario
--------------------------------

The flow of development using Jubatus Client is following:

 1. Connection settings to ``jubaclassifier``

  Setting the HOST and RPC port of ``jubaclassifier`` .

 2. Prepare the training data

  Make some pair of class and features.

 3. Data training (update the model)

  Send the training data to ``jubaclassifier`` using ``train`` method.

 4. Prepare the test data

  Make the feature data.

 5. Classify the test data

  Send the test data to ``jubaclassifier`` using ``classify`` method.

 6. Output the result

  Compare the score value of each classes. And output the class with highest score.


--------------------------------
Sample Program
--------------------------------

.. toctree::
   :maxdepth: 2

   classifier_python
   classifier_ruby
   classifier_java

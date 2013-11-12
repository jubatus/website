Java
==========================

Here we explain the Java sample program of Classifier.

--------------------------------
Source_code
--------------------------------

In this sample program, we will explain 1) how to configure the learning-algorithms that used by Jubatus, with the example file 'gender.json'; 2) how to learn the training data and make predictions based on them, with the example file ‘GenderMain.java’. Here are the source codes of 'gender.json' and 'GenderMain.java'.

**gender.json**

.. code-block:: js
 :linenos:

 {
   "method": "AROW",
   "converter": {
     "num_filter_types": {},
     "num_filter_rules": [],
     "string_filter_types": {},
     "string_filter_rules": [],
     "num_types": {},
     "num_rules": [],
     "string_types": {
       "unigram": { "method": "ngram", "char_num": "1" }
     },
     "string_rules": [
       { "key": "*", "type": "unigram", "sample_weight": "bin", "global_weight": "bin" }
     ]
   },
   "parameter": {
     "regularization_weight" : 1.0
   }
 }

**GenderMain.java**

.. code-block:: java
 :linenos:

 package us.jubat.example.gender;

 import java.util.ArrayList;
 import java.util.Arrays;
 import java.util.List;

 import us.jubat.classifier.ClassifierClient;
 import us.jubat.classifier.EstimateResult;
 import us.jubat.classifier.LabeledDatum;
 import us.jubat.common.Datum;

 public class GenderMain {

     private static Datum makeDatum(String hair, String top, String bottom,
             double height) {
         return new Datum().addString("hair", hair)
             .addString("top", top)
             .addString("bottom", bottom)
             .addNumber("height", height);
     }

     private static LabeledDatum makeTrainDatum(String label, String hair,
             String top, String bottom, double height) {
         return new LabeledDatum(label, makeDatum(hair, top, bottom, height));
     }

     public static void main(String[] args) throws Exception {
         String host = "127.0.0.1";
         int port = 9199;
         String name = "test";

         ClassifierClient client = new ClassifierClient(host, port, name, 1);

         LabeledDatum[] trainData = { //
         makeTrainDatum("male", "short", "sweater", "jeans", 1.70),
                 makeTrainDatum("female", "long", "shirt", "skirt", 1.56),
                 makeTrainDatum("male", "short", "jacket", "chino", 1.65),
                 makeTrainDatum("female", "short", "T shirt", "jeans", 1.72),
                 makeTrainDatum("male", "long", "T shirt", "jeans", 1.82),
                 makeTrainDatum("female", "long", "jacket", "skirt", 1.43),
                 // makeTrainDatum("male", "short", "jacket", "jeans", 1.76),
                 // makeTrainDatum("female", "long", "sweater", "skirt", 1.52),
                 };

         client.train(Arrays.asList(trainData));

         Datum[] testData = { //
         makeDatum("short", "T shirt", "jeans", 1.81),
                 makeDatum("long", "shirt", "skirt", 1.50), };

         List<List<EstimateResult>> results = client.classify(
                 Arrays.asList(testData));

         for (List<EstimateResult> result : results) {
             for (EstimateResult r : result) {
                 System.out.printf("%s %f\n", r.label, r.score);
             }
             System.out.println();
         }

         System.exit(0);
     }
 }

--------------------------------
Explanation
--------------------------------

**gender.json**

The configuration information is given by the JSON unit. Here is the meaning of each JSON filed.

 * method

  Specify the algorithm used in Classification. In this example, the AROW (Adaptive Regularization of Weight vectors) is used.

 * converter

  Specify the configurations in feature converter. In this sample, we will classify a person into male or female through the features of 'length of hair', 'top clothes', 'bottom clothese' and 'height'. The "string_values" and "num_values" are stored in key-value pairs without using "\*_filter_types" configuration.

 * parameter

  Specify the parameter that passed to the algorithm. The parameter varis when the method is changed. In this example, the method is specified as 'AROW', with [regularization_weight: 1.0]. In addition, the parameter 'regularization_weight' in different algorithms plays different roles and affects differently, so please pay attention to setting the value of it for each algorithm. When 'regularization_weight' parameter becomes bigger, the learning spead will increase, while the noice will decrease.

**GenderMain.java**

We explain the learning and prediction processes in this example codes.

First of all, to write the Client program for Classifier, we can use the ClassifierClient class defined in 'us.jubat.classifier'. There are two methods used in this program. The 'train' method for learning process, and the 'classify' method for prediction with the data learnt.

 1. How to connect to Jubatus Server

  Connect to Jubatus Server (Line 32).
  Setting the IP addr, RPC port of Jubatus Server, the unique name for task identification in Zookeeper and the value of request timeout.

 2. Prepare the learning data

  Make a dataset for the data to be learnt (Line 34-43).

  The dataset is input into the train() method in ClassifierClient, for the learning process. The figure below shows the structure of the data being leant.


  +----------------------------------------------------------------------------------------------------+
  |LabeledDatum[]                                                                                      |
  +-------------+--------------------------------------------------------------------------------------+
  |label(String)|Datum                                                                                 |
  +-------------+----------------------------+----------------------------+----------------------------+
  |             |List<StringValue>           |List<NumValue>              |List<BinaryValue>           |
  +-------------+------------+---------------+------------+---------------+------------+---------------+
  |             |key(String) |value(String)  |key(String) |value(double)  |key(String) |value(byte[])  |
  +=============+============+===============+============+===============+============+===============+
  |"male"       | | "hair"   | | "short"     | "height"   | 1.70          |            |               |
  |             | | "top"    | | "sweater"   |            |               |            |               |
  |             | | "bottom" | | "jeans"     |            |               |            |               |
  +-------------+------------+---------------+------------+---------------+------------+---------------+
  |"female"     | | "hair"   | | "long"      | "height"   | 1.56          |            |               |
  |             | | "top"    | | "shirt"     |            |               |            |               |
  |             | | "bottom" | | "skirt"     |            |               |            |               |
  +-------------+------------+---------------+------------+---------------+------------+---------------+
  |"male"       | | "hair"   | | "short"     | "height"   | 1.65          |            |               |
  |             | | "top"    | | "jacket"    |            |               |            |               |
  |             | | "bottom" | | "chino"     |            |               |            |               |
  +-------------+------------+---------------+------------+---------------+------------+---------------+
  |"female"     | | "hair"   | | "short"     | "height"   | 1.72          |            |               |
  |             | | "top"    | | "T shirt"   |            |               |            |               |
  |             | | "bottom" | | "jeans"     |            |               |            |               |
  +-------------+------------+---------------+------------+---------------+------------+---------------+
  |"male"       | | "hair"   | | "long"      | "height"   | 1.82          |            |               |
  |             | | "top"    | | "T shirt"   |            |               |            |               |
  |             | | "bottom" | | "jeans"     |            |               |            |               |
  +-------------+------------+---------------+------------+---------------+------------+---------------+
  |"feale"      | | "hair"   | | "long"      | "height"   | 1.43          |            |               |
  |             | | "top"    | | "jacket"    |            |               |            |               |
  |             | | "bottom" | | "skirt"     |            |               |            |               |
  +-------------+------------+---------------+------------+---------------+------------+---------------+

  trainData is the array of LabeledDatum. LabeledDatum is a pair of Datum and its label. In this sample, the label demonstrates the class name each Datum belongs to. Each Datum stores the data in key-value pairs, which is the format readable by Jubatus. The key can be recognized as the feature vector. Inside the Datum, there are 3 kinds of key-value lists, string_values, num_values and binary_values. Each of these uses StringValue class, NumValue class and BinaryValue class. For example, the "hair", "top", "bottom" values are StirngValue, While the "height" value is NumValue. Therefore, they are stored separately inside each Datum.

  Here is the procedure of making study data.

  To make study data, the private method "makeTrainDatum" is used (Line 22-25).

  In this example, the key-value lists have the keys of "hair", "top", and "bottom" and their String type values registered through addString method, for example, are "short", "sweater", and "jeans". In addition, The key-value list have the key of "height", and its double type value registered through addNumber method, for example, "1.70" (Line 16-19).

  According to the flow above, the training data is generated.

 3. Model training (update learning model)

  We train our learning model by using the method train() (Line 45), with the data generated in step.2 above.

 4. Prepare the prediction data

  Different from training data, prediction data does not contain "lable", and it is only stored in the Datum unit by using makeDatum() (Line 14-20).

 5. Data prediction

  By inputting the testData generated in step.4 into the classify() method of ClassifierClient (Line 51-52), the prediction result will be stored in the EstimateResult List (Line 55). EstimateResult contains label and score means the confidence of each label (Line 56).


------------------------------------
Run the sample program
------------------------------------

［At Jubatus Server］
 start "jubaclassifier" process.

::

 $ jubaclassifier --configpath gender.json

［At Jubatus Client］
 Get the required package and Java client ready.
 Run!


Java
================================

Here we explain the sample program of Regression in Java. 

--------------------------------
Source_code
--------------------------------

In this sample program, we will explain 1) how to configure the learning-algorithms that used by Jubatus, with the example file 'rent.json'; 2) how to train the model by 'rent.java' with the training data in 'rent-data.csv' file, and how to predict with the estimation data in 'myhome.yml' file. Here are the source codes of 'rent.json', 'rent.java' and 'myhome.yml'.


**rent.json**

.. code-block:: java

 01 : {
 02 :   "method": "PA",
 03 :   "converter": {
 04 :     "num_filter_types": {},
 05 :     "num_filter_rules": [],
 06 :     "string_filter_types": {},
 07 :     "string_filter_rules": [],
 08 :     "num_types": {},
 09 :     "num_rules": [
 10 :       { "key": "*", "type": "num" }
 11 :     ],
 12 :     "string_types": {},
 13 :     "string_rules": [
 14 :       { "key": "aspect", "type": "str", "sample_weight": "bin", "global_weight": "bin" }
 15 :     ]
 16 :   },
 17 :   "parameter": {
 18 :     "sensitivity": 0.1,
 19 :     "regularization_weight": 3.402823e+38
 20 :   }
 21 : }

**rent.java**

.. code-block:: java

 001 : package rent;
 
 002 : import java.io.BufferedReader;
 003 : import java.io.File;
 004 : import java.io.FileNotFoundException;
 005 : import java.io.FileReader;
 006 : import java.io.IOException;
 007 : import java.math.BigDecimal;
 008 : import java.util.ArrayList;
 009 : import java.util.Arrays;
 010 : import java.util.Collections;
 011 : import java.util.List;
 012 : import java.util.Map;
 013 : import java.util.HashMap;
 014 : import org.ho.yaml.Yaml;
 015 : import us.jubat.regression.Datum;
 016 : import us.jubat.regression.RegressionClient;
 017 : import us.jubat.regression.TupleFloatDatum;
 018 : import us.jubat.regression.TupleStringDouble;
 019 : import us.jubat.regression.TupleStringString;

 020 : public class rent {
 021 : 	public static final String HOST = "127.0.0.1";
 022 : 	public static final int PORT = 9199;
 023 : 	public static final String NAME = "rent";
 024 : 	public static final String FILE_PATH = "./src/main/resources/";

 025 : 	// Definie the column name in CSV file
 026 : 	public static String[] CSV_COLUMN = {
 027 : 		"rent",
 028 : 		"distance",
 029 : 		"space",
 030 : 		"age",
 031 : 		"stair",
 032 : 		"aspect"
 033 : 		};

 034 : 	// Item in String type
 035 : 	public static String[] STRING_COLUMN = {
 036 : 		"aspect"
 037 : 		};

 038 : 	// Items in Double type
 039 : 	public static String[] DOUBLE_COLUMN = {
 040 : 		"distance",
 041 : 		"space",
 042 : 		"age",
 043 : 		"stair",
 044 : 		};

 045 : 	public void update(String cvsName) throws Exception {
 046 : 		// 1. Connect to Jubatus Server
 047 : 		RegressionClient client = new RegressionClient(HOST, PORT, 5);

 048 : 		// 2. Prepare the training data
 049 : 		List<TupleFloatDatum> trainData = new ArrayList<TupleFloatDatum> ();
 050 : 		Datum datum = null;

 051 : 		 try {
 052 : 			File csv = new File(FILE_PATH + cvsName ); // CSV Data File
 053 : 			BufferedReader br = new BufferedReader(new FileReader(csv));
 054 : 			List<String> strList = new ArrayList<String> ();
 055 : 			List<String> doubleList = new ArrayList<String> ();
 056 : 			String line = "";

 057 : 			// read data line by line, until the last one.
 058 : 			while ((line = br.readLine()) != null) {
 059 : 				strList.clear();
 060 : 				doubleList.clear();
 061 : 				TupleFloatDatum train = new TupleFloatDatum();

 062 : 				// split the data in one line into items
 063 : 				String[] strAry = line.split(",");

 064 : 				// check the number of CSV columns and the comment
 065 : 				if( strAry.length != CSV_COLUMN.length || strAry[0].startsWith("#")){
 066 : 					continue;
 067 : 				}

 068 : 				// make lists for String and Double items
 069 : 				for (int i=0; i<strAry.length; i++) {
 070 : 					if(Arrays.toString(STRING_COLUMN).contains(CSV_COLUMN[i])){
 071 : 						strList.add(strAry[i]);
 072 : 					} else if(Arrays.toString(DOUBLE_COLUMN).contains(CSV_COLUMN[i])){
 073 : 						doubleList.add(strAry[i]);
 074 : 					}
 075 : 				}
 
 076 : 				// make datum
 077 : 				datum = makeDatum(strList, doubleList);
 078 : 				train.first = Float.parseFloat(strAry[0]);
 079 : 				train.second = datum;
 080 : 				trainData.add(train);
 081 : 			}
 082 : 			br.close();

 083 : 			// shuffle the training data
 084 : 			Collections.shuffle(trainData);

 085 : 			// 3. Data training (update model)
 086 : 			int trainCount = client.train( NAME, trainData);
 087 : 			System.out.print("train ... " + trainCount + "\n");
 088 : 		 } catch (FileNotFoundException e) {
 089 : 			 // catch the exception in File object creation
 090 : 			 e.printStackTrace();
 091 : 		 } catch (IOException e) {
 092 : 			 // catch the exception when closing BufferedReader object
 093 : 			 e.printStackTrace();
 094 : 		 }
 095 : 		return;
 096 : 	}

 097 : 	@SuppressWarnings("unchecked")
 098 : 	public void analyze(String yamlName) throws Exception {
 099 : 		RegressionClient client = new RegressionClient(HOST, PORT, 5);

 100 : 		// 4. Prepare the estimation data
 101 : 		List<Datum> datumList = new ArrayList<Datum> ();

 102 : 		// result list
 103 : 		List<Float> result = new ArrayList<Float> ();
 104 : 		try {
 105 : 			// read the configuration from YAML file
 106 : 			Map<String, Object> hash = (HashMap<String, Object>) Yaml.load(new File(FILE_PATH + yamlName ));

 107 : 			// make the estimation data
 108 : 			datumList.add(makeDatum(hash));

 109 : 			// 5. Predict by the model learned
 110 : 			result.addAll(client.estimate( NAME, datumList));

 111 : 			// change the result into BigDecimal type
 112 : 			BigDecimal bd = new BigDecimal(result.get(0));
 113 : 			// rounding at the 2nd decimal
 114 : 			BigDecimal bd2 = bd.setScale(1, BigDecimal.ROUND_HALF_UP);

 115 : 			// 6. Output result
 116 : 			System.out.print("rent .... " + bd2 );

 117 : 		} catch (FileNotFoundException e) {
 118 : 			 // capture the exception in File object creation.
 119 : 			 e.printStackTrace();
 120 : 		}
 121 : 		return;
 122 : 	}

 123 : 	// Create the lists with the name given in the Datum (for list)
 124 : 	private Datum makeDatum(List<String> strList, List<String> doubleList) {

 125 : 		Datum datum = new Datum();
 126 : 		datum.string_values = new ArrayList<TupleStringString>();
 127 : 		datum.num_values = new ArrayList<TupleStringDouble>();

 128 : 		for( int i = 0 ; i < strList.size() ; i++) {
 129 : 			TupleStringString data = new TupleStringString();
 130 : 			data.first = STRING_COLUMN[i];
 131 : 			data.second = strList.get(i);
 132 : 			datum.string_values.add(data);
 133 : 		}

 134 : 		try {
 135 : 			for( int i = 0 ; i < doubleList.size() ; i++) {
 136 : 				TupleStringDouble data = new TupleStringDouble();
 137 : 				data.first = DOUBLE_COLUMN[i];
 138 : 				data.second = Double.parseDouble(doubleList.get(i));
 139 : 				datum.num_values.add(data);
 140 : 			}
 141 : 		} catch (NumberFormatException e){
 142 : 			e.printStackTrace();
 143 : 			return null;
 144 : 		}
 145 : 		return datum;
 146 : 	}

 147 : 	// Create the lists with the name given in the Datum (for Map)
 148 : 	private Datum makeDatum(Map<String, Object> hash) {

 149 : 		Datum datum = new Datum();
 150 : 		datum.string_values = new ArrayList<TupleStringString>();
 151 : 		datum.num_values = new ArrayList<TupleStringDouble>();

 152 : 		for( int i = 0 ; i < STRING_COLUMN.length ; i++) {
 153 : 			// Insert into Datum only if it is contained by HashMap and not NULL
 154 : 			if( hash.containsKey(STRING_COLUMN[i]) && hash.get(STRING_COLUMN[i]) != null ) {
 155 : 				TupleStringString data = new TupleStringString();
 156 : 				data.first = STRING_COLUMN[i];
 157 : 				data.second = hash.get(STRING_COLUMN[i]).toString();
 158 : 				datum.string_values.add(data);
 159 : 			}
 160 : 		}

 161 : 		try {
 162 : 			for( int i = 0 ; i < DOUBLE_COLUMN.length ; i++) {
 163 : 				// Insert into Datum only if it is contained by HashMap and not NULL
 164 : 				if( hash.containsKey(DOUBLE_COLUMN[i]) && hash.get(DOUBLE_COLUMN[i]) != null ) {
 165 : 					TupleStringDouble data = new TupleStringDouble();
 166 : 					data.first = DOUBLE_COLUMN[i];
 167 : 					data.second = Double.parseDouble(hash.get(DOUBLE_COLUMN[i]).toString());
 168 : 					datum.num_values.add(data);
 169 : 				}
 170 : 			}
 171 : 		} catch (NumberFormatException e){
 172 : 			e.printStackTrace();
 173 : 			return null;
 174 : 		}
 175 : 		return datum;
 176 : 	}
 
 177 : 	// Main methods
 178 : 	public static void main(String[] args) throws Exception {
 179 : 		if(args.length < 1){
 180 : 			System.out.print("Please set the arguments.\n" +
 181 : 							"1st argument： YML file name (required)\n" +
 182 : 							"2nd argument： CSV file name (when there is training data)\n");
 183 : 			return;
 184 : 		}
 185 : 		// when there is the 2nd argument, start the update method for model training.
 186 : 		if(args.length > 1 && !"".equals(args[1])){
 187 : 			new rent().update(args[1]);
 188 : 		}
 189 : 		if(!"".equals(args[0])){
 190 : 			new rent().analyze(args[0]);
 191 : 		}
 192 : 		System.exit(0);
 193 : 	}
 194 : }
 

**myhome.yml**

::

 01 :  #
 02 :  # distance : distance from station (walking time in minutes)
 03 :  # space    : the footprint of the house (m*m)
 04 :  # age      : build age (year)
 05 :  # stair    : floors
 06 :  # aspect   : direction [ N / NE / E / SE / S / SW / W / NW ]
 07 :  #
 08 :  distance : 8
 09 :  space    : 32.00
 10 :  age      : 15
 11 :  stair    : 5
 12 :  aspect   : "S"


--------------------------------
Explanation
--------------------------------

**rent.json**

The configuration information is given by the JSON unit. Here is the meaning of each JSON filed.

* method

 Specify the algorithm used in regression. 
 Currently, we have "PA" (Passive Aggressive) only, so we specify it with "PA".

* converter

 Specify the configurations in feature converter.
 In this example, we will set the "num_rules" and "string_rules".
 
 "num_rules" are used to specify the extraction rules of numercial features.
 "key" is "*", it means all the "key" are taken into consideration, "type" is "num", it means the number(value) specified will be directly used as the input for training the model. 
 For example, if the "age = 2", use 2 as the input; if the "stair = 6", use 6 as the input.

 "string_rules" are used to specify the extraction rules of string features.
 Here, "key = aspect", "type = str", "sample_weight = bin", and "global_weight = bin".
 Their meaning are: the "aspect" is treated as a string, and used as the input feature without reform; the weight of each key-value feature is specified to be "1"; and the global weight of each feature is specified to be "1".

* parameter

 Specify the parameters to be passed to the algorithm.
 The method specified here is "PA", with its configuration as ""sensitivity" and "regularization_weight".
 
 "sensitivity" specifies the tolerable range of error. When its value increases, it becomes resistant to noise, but makes errors remain easily instead.
 "regularization_weight" specifies the sensitivity parameter in the learning. When its value increases, the learning becomes faster, but the method become susceptible to the noise.
 
 In addition, the "regularization_weight" above plays various roles in different algorithms, so please be careful in configuring its values in different algorithms.


**rent.java**

We explain the learning and prediction processes in this example.

 To write the Client program for Regression, we can use the RegressionClient class defined in 'us.jubat.regression'. There are two methods used in this program. The 'train' method for learning process, and the 'estimate' method for prediction with the data learnt.
 
 1. Connect to Jubatus Server

  Connect to Jubatus Server (Line 47)
  Setting the IP addr., RPC port of Jubatus Server, and the connection waiting time.

 2. Prepare the training data

  RegressionClient puts the training data into a TupleFloatDatum List, and sends the data to train() methods for the model training.
  In this example, the training data is generated from the CSV file that privided by a housing rental website. 
  Factors in the rental information includes rent, aspect, distance, space, age and stairs.
  Figure below shows the training data. (The following are four examples from over one hundred housing info. listed in the rent-data.csv)
  
  +----------------------------------------------------------------------+
  |                         TupleFloatDatum                              |
  +-------------+--------------------------------------------------------+
  |label(Float) |Datum                                                   |
  |             +--------------------------+-----------------------------+
  |             |TupleStringString(List)   |TupleStringDoubel(List)      |
  |             +------------+-------------+---------------+-------------+
  |             |key(String) |value(String)|key(String)    |value(double)|
  +=============+============+=============+===============+=============+
  |5.0          |"aspect"    |"SW"         | | "distance"  | | 10        |
  |             |            |             | | "space"     | | 20.04     |
  |             |            |             | | "age"       | | 12        |
  |             |            |             | | "stair"     | | 1         |
  +-------------+------------+-------------+---------------+-------------+
  |6.3          |"aspect"    |"N"          | | "distance"  | | 8         |
  |             |            |             | | "space"     | | 21.56     |
  |             |            |             | | "age"       | | 23        |
  |             |            |             | | "stair"     | | 2         |
  +-------------+------------+-------------+---------------+-------------+
  |7.5          |"aspect"    |"SE"         | | "distance"  | | 25        |
  |             |            |             | | "space"     | | 22.82     |
  |             |            |             | | "age"       | | 23        |
  |             |            |             | | "stair"     | | 4         |
  +-------------+------------+-------------+---------------+-------------+
  |9.23         |"aspect"    |"S"          | | "distance"  | | 10        |
  |             |            |             | | "space"     | | 30.03     |
  |             |            |             | | "age"       | | 0         |
  |             |            |             | | "stair"     | | 2         |
  +-------------+------------+-------------+---------------+-------------+

  TupleFloatDatum contains 2 fields, "Datum" and the "label".
  "Datum" is composed of key-value data which could be processed by Jubatus, and there are 2 types of key-value data format.
  In the first type, both the "key" and "value" are in string format (string_values); in the second one, the "key" is in string format, but the "value" is in numerical format (num_values).
  These two types are represented in TupleStringString class and TupleStringDouble class, respectively.
  
  | Please have a view of the first example data in this table. Because the "aspect" is in string format, it is stored in the first list of the TupleStringString class
  | in which, the key is set as "aspect", value is set as "SW".
  | Because other items are numerical, they are stored in the list of the TupleStringDouble class, in which
  | the first list's key is set as "distance" and value is set as "10",
  | the second list's key is set as "space" and value is set as "20.04",
  | the third list's key is set as "age" and value is set as "15",
  | the fourth list's key is set as "stair" and value is set as "1".
   
  The Datum of these 5 Lists is appended with a label of "5.0", as its rent, and forms an instance of TupleFloatDatum class which retains the rent (of 5.0 * 10,000) and its corresponding housing condition info.
  Thus, the housing rental data are generated in the format of (TupleFloatDatum) List, as the training data to be used.
    
  Here is the detailed process for making the training data in this sample.
  
  First, declare the variable of training data "trainDat", as a TupleFloatDatum List (Line 49).
  Next, read the source file (CSV file) of the training data.
  Here, FileReader() and BuffererdReader() is used to read the items in CVS file line by line (Line 57-81).
  Split the data read from each line in CSV file, by the ',' mark (Line 63).
  Using the defined CSV item list (CSV_COLUMN),String item list (STRING_COLUMN) and Double item list (Double_COLUMN) to transfer the CSV data into strList or doubleList, if the item is in String or Double type (Line 64-75).
  Then, create the "Datum" by using the 2 lists, as the arguments in the private method of [makeDatum] (Line 77).
   
  The string item list and double item list in the arguments of [makeDatum] method are used to generate the TupleStringString list and TupleStringDouble list, respecitively (Line 124-146).
  At first, create the instance of Datum class component: "string_values" list and "num_values" list (Line 126-127).
  Next, generate the TupleStringString by reading the items from strList. The first element is the column name (as the key), and the second element is the value. The data is added into the string_values list (Line 129-132).
  The Double type items are processed in the similar way as String type items, to generate TupleStringDouble. Please note that the elements of num_values are added with type conversion, because the argument is of String type List while the num_values in Datum is of Double type (Line 138).
  Now, the Datum is created.
  
  The Datum created in [makeDatum] above is appended with the rent label, so as to be used as one piece of training data (argument 'train' in Line 78-79).
  By looping the above processes, source data in the CSV file will be transferred into the training data line by line and stored in the trainData List (Line 80).

 3. Model Training (update learning model

  Input the training data generated in step.2 into the train() method (Line 86).
  The first parameter in train() is the unique name for task identification in Zookeeper.
  (use null charactor "" for the stand-alone mode)
  The second parameter specifies the Datum generated in step.2.
  The returned result is the number of training data have been processed.
  
 
 4. Prepare the prediction data 

  Prepare the prediction data in the similar way of training Datum creation.
  Here, we generate the data for prediction by using the YAML file (please download the library `JYaml <http://jyaml.sourceforge.net/download.html>`_ )
  YAML is one kind of data format, in which objects and structure data are serialized.
  
  Read the YAML file (myhome.yml) as a HashMap (Line 106).
  Generate the prediction Datum by using the [makeDatum] method, as simliar as Step 2, with the HashMap.
  
  However, since the argument used here is HashMap, although the output is the same, the generation process is different (Line 148-176).
  In addition, there is no need to fill all the items in one Datum. The only required conditions are created in the Datum. 
  
  Add the Datum into the prediction data list, and send it into the estimate() method in "RegressionClient" for prediction.
  
 5. Prediction by the regression model

  The prediction results are returned as a list by the estimate() method (Line 116).

 6. Output the result

  The prediction results are returned in the same order of the prediction data. (In this sample, only one prediction data is used, thus only one result is returned.)
  The result is rounded at 2nd decimal for output, because it is in Float type.

-----------------------------------
Run the sample program
-----------------------------------

**[At Jubatus Server]**
 
 start "jubaregression" process.

 ::

  $ jubaregression --configpath rent.json

**[At Jubatus Client]**

 Get the required package and Java client ready.
 | Specify the arguments and Run! (The 2nd arguments is optional.)
 |  The first argument: YML file name (required)
 |  The second argument: CSV file name (if there is training data)
 

**[Result]**


 ::

  train ... 145
  rent .... 9.9

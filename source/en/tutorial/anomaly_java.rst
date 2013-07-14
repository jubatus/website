Java
==================

Here we explain the java sample program of anomaly detection.

--------------------------------
Source_code
--------------------------------

In this sample program, we will explain 1) how to configure the learning-algorithms in Jubatus with the config file 'config.json'; 2) how to detect the anomaly data with the example file ‘lof.java’. Here are the source codes of 'config.json' and 'lof.java'.

**config.json**

.. code-block:: java

 01 : {
 02 :  "method" : "lof",
 03 :  "parameter" : {
 04 :   "nearest_neighbor_num" : 10,
 05 :   "reverse_nearest_neighbor_num" : 30,
 06 :   "method" : "euclid_lsh",
 07 :   "parameter" : {
 08 :    "lsh_num" : 8,
 09 :    "table_num" : 16,
 10 :    "probe_num" : 64,
 11 :    "bin_width" : 10,
 12 :    "seed" : 1234,
 13 :    "retain_projection" : true
 14 :   }
 15 :  },
 
 16 :  "converter" : {
 17 :   "string_filter_types": {},
 18 :   "string_filter_rules": [],
 19 :   "num_filter_types": {},
 20 :   "num_filter_rules": [],
 21 :   "string_types": {},
 22 :   "string_rules": [{"key":"*", "type":"str", "global_weight" : "bin", "sample_weight" : "bin"}],
 23 :   "num_types": {},
 24 :   "num_rules": [{"key" : "*", "type" : "num"}]
 25 :  }
 26 : }

 

**anomaly.java**

.. code-block:: java

 001 : package lof;
 
 002 : import java.io.BufferedReader;
 003 : import java.io.FileNotFoundException;
 004 : import java.io.FileReader;
 005 : import java.io.IOException;
 006 : import java.util.ArrayList;
 007 : import java.util.Arrays;
 008 : import java.util.List;
 009 : import us.jubat.anomaly.*;
 
 010 : public class Lof {
 011 : 	public static final String HOST = "127.0.0.1";
 012 : 	public static final int PORT = 9199;
 013 : 	public static final String NAME = "anom_kddcup";
 014 : 	public static final String FILE_PATH = "./src/main/resources/";
 015 : 	public static final String TEXT_NAME = "kddcup.data_10_percent.txt";
 
 016 : 	// declare all the data items consisted in each piece of training data
 017 : 	public static String[] TEXT_COLUMN = {
 018 : 		"duration",
 019 : 		"protocol_type",
 020 : 		"service",
 021 : 		"flag",
 022 : 		"src_bytes",
 023 : 		"dst_bytes",
 024 : 		"land",
 025 : 		"wrong_fragment",
 026 : 		"urgent",
 027 : 		"hot",
 028 : 		"num_failed_logins",
 029 : 		"logged_in",
 030 : 		"num_compromised",
 031 : 		"root_shell",
 032 : 		"su_attempted",
 033 : 		"num_root",
 034 : 		"num_file_creations",
 035 : 		"num_shells",
 036 : 		"num_access_files",
 037 : 		"num_outbound_cmds",
 038 : 		"is_host_login",
 039 : 		"is_guest_login",
 040 : 		"count",
 041 : 		"srv_count",
 042 : 		"serror_rate",
 043 : 		"srv_serror_rate",
 044 : 		"rerror_rate",
 045 : 		"srv_rerror_rate",
 046 : 		"same_srv_rate",
 047 : 		"diff_srv_rate",
 048 : 		"srv_diff_host_rate",
 049 : 		"dst_host_count",
 050 : 		"dst_host_srv_count",
 051 : 		"dst_host_same_srv_rate",
 052 : 		"dst_host_diff_srv_rate",
 053 : 		"dst_host_same_src_port_rate",
 054 : 		"dst_host_srv_diff_host_rate",
 055 : 		"dst_host_serror_rate",
 056 : 		"dst_host_srv_serror_rate",
 057 : 		"dst_host_rerror_rate",
 058 : 		"dst_host_srv_rerror_rate",
 059 : 		"label"
 060 : 	};
 
 061 : 	// items in String type
 062 : 	public static String[] STRING_COLUMN = {
 063 : 		"protocol_type",
 064 : 		"service",
 065 : 		"flag",
 066 : 		"land",
 067 : 		"logged_in",
 068 : 		"is_host_login",
 069 : 		"is_guest_login"
 070 : 	};
 
 071 : 	// items in Double type
 072 : 	public static String[] DOUBLE_COLUMN = {
 073 : 		"duration",
 074 : 		"src_bytes",
 075 : 		"dst_bytes",
 076 : 		"wrong_fragment",
 077 : 		"urgent",
 078 : 		"hot",
 079 : 		"num_failed_logins",
 080 : 		"num_compromised",
 081 : 		"root_shell",
 082 : 		"su_attempted",
 083 : 		"num_root",
 084 : 		"num_file_creations",
 085 : 		"num_shells",
 086 : 		"num_access_files",
 087 : 		"num_outbound_cmds",
 088 : 		"count",
 089 : 		"srv_count",
 090 : 		"serror_rate",
 091 : 		"srv_serror_rate",
 092 : 		"rerror_rate",
 093 : 		"srv_rerror_rate",
 094 : 		"same_srv_rate",
 095 : 		"diff_srv_rate",
 096 : 		"srv_diff_host_rate",
 097 : 		"dst_host_count",
 098 : 		"dst_host_srv_count",
 099 : 		"dst_host_same_srv_rate",
 100 : 		"dst_host_same_src_port_rate",
 101 : 		"dst_host_diff_srv_rate",
 102 : 		"dst_host_srv_diff_host_rate",
 103 : 		"dst_host_serror_rate",
 104 : 		"dst_host_srv_serror_rate",
 105 : 		"dst_host_rerror_rate",
 106 : 		"dst_host_srv_rerror_rate"
 107 : 	};
 
 108 : 	public void execute() throws Exception {
 109 : 		// 1. Connect to Jubatus Server
 110 : 		AnomalyClient client = new AnomalyClient(HOST, PORT, 5);
 
 111 : 		// 2. Prepare learning data
 112 : 		Datum datum = null;
 113 : 		TupleStringFloat result = null;
  
 114 : 		try {
 115 : 			BufferedReader br = new BufferedReader(new FileReader(FILE_PATH + TEXT_NAME));
 116 : 			List<String> strList = new ArrayList<String>();
 117 : 			List<String> doubleList = new ArrayList<String>();
 118 : 			String line = "";
 
 119 : 			// read the data row by row until the last one
 120 : 			while ((line = br.readLine()) != null) {
 121 : 				strList.clear();
 122 : 				doubleList.clear();
 
 123 : 				// split the data items in each row
 124 : 				String[] strAry = line.split(",");
 
 125 : 				// make the String and Double Lists to store the data items 
 126 : 				for (int i = 0; i < strAry.length; i++) {
 127 : 					if (Arrays.toString(STRING_COLUMN).contains(TEXT_COLUMN[i])) {
 128 : 						strList.add(strAry[i]);
 129 : 					} else if (Arrays.toString(DOUBLE_COLUMN).contains(TEXT_COLUMN[i])) {
 130 : 						doubleList.add(strAry[i]);
 131 : 					}
 132 : 				}
 
 133 : 				// make the datum
 134 : 				datum = makeDatum(strList, doubleList);
  
 135 : 				// 3. Model training(update learning model)
 136 : 				result = client.add(NAME, datum);

 137 : 				// 4. Display result
 138 : 				if ( !(Float.isInfinite(result.second)) && result.second != 1.0) {
 139 : 					System.out.print( "('" + result.first + "', " + result.second + ") " + strAry[strAry.length -1] + "\n" );
 140 : 				}
 141 : 			}
 142 : 			br.close();
 143 : 		} catch (FileNotFoundException e) {
 144 : 			// capture the exception in File object creation
 145 : 			e.printStackTrace();
 146 : 		} catch (IOException e) {
 147 : 			// capture the exception in closing BufferedReader object
 148 : 			e.printStackTrace();
 149 : 		}
 150 : 		return;
 151 : 	}
 
 152 : 	// Make the Datum with the assigned lists
 153 : 	private Datum makeDatum(List<String> strList, List<String> doubleList) {

 154 : 		Datum datum = new Datum();
 155 : 		datum.string_values = new ArrayList<TupleStringString>();
 156 : 		datum.num_values = new ArrayList<TupleStringDouble>();
 
 157 : 		for (int i = 0; i < strList.size(); i++) {
 158 : 			TupleStringString data = new TupleStringString();
 159 : 			data.first = STRING_COLUMN[i];
 160 : 			data.second = strList.get(i);
 161 : 			datum.string_values.add(data);
 162 : 		}
 
 163 : 		try {
 164 : 			for (int i = 0; i < doubleList.size(); i++) {
 165 : 				TupleStringDouble data = new TupleStringDouble();
 166 : 				data.first = DOUBLE_COLUMN[i];
 167 : 				data.second = Double.parseDouble(doubleList.get(i));
 168 : 				datum.num_values.add(data);
 169 : 			}
 170 : 		} catch (NumberFormatException e) {
 171 : 			e.printStackTrace();
 172: 			return null;
 173 : 		}
 174 : 		return datum;
 175 : 	}
 
 176 : 	// main method
 177 : 	public static void main(String[] args) throws Exception {
 178 : 		new Lof().execute();
 179 : 		System.exit(0);
 180 : 	}
 181 : }

--------------------------------
Explanation
--------------------------------

**config.json**

The configuration information is given by the JSON unit. Here is the meaning of each JSON filed.

 * method

  Specify the algorithm used in anomaly detection. Currently, "LOF"(Local Outlier Factor) is the only one algorithm for anomaly detection, so, we write "LOF" here.

 * converter
 
  Specify the configurations in feature converter. In this sample, we will set "num_rules" and "string_rules". 

  "num_rules" specifies the value extracting rules for values in numerical format.
  "key" is set as "*" here, which means all the "key" will be taken into account. "type" is set as "num", which means each value has its weight as equal as the value itself. For example, if data's value i "2", its weight is set as 2; if data's value is "6", its weight is set as 6.

 
  "string_rules" specifies the value extracting rules for values in string format.
  Here, "key" is set as "*", "type" is "str", "sample_weight" is "bin", and "global_weight" is "bin".
  This means, all the "key" will be taken into account, the features in strings values will be used without convertion, the weight of each key-value will be calculated throughout the whole data have been used, and the global weight is a constant value of "1".

 * parameter(could be modified)

 ･･･
  

**anomaly.java**

 anomaly.java will extract the data from text file, send them to Jubatus server, and get their anomaly detection result from the server.

 1. Connect to Jubatus Server

  Connect to Jubatus Server (Line 110).
  Setting the IP addr., RPC port of Jubatus Server, and the connection waiting time.

 2. Prepare the learning data

  AnomalyClient will send the Datum to Jubatus server for data learning or anomaly detection, by using its "add" method.
  In this example, the result-data in KDD Cup(Knowledge Discovery and Data Mining Cup) is used as the trainning data. At first, the program read the training data from the TEXT file, one line at a time, by using FileReader() and BuffererdReader() methods (Line 120-134). The data in TEXT file are seperated by commas, so we split the items by ’,’ (Line 124).
  By using the whole items definition list: TEXT file(TEXT_COLUMN); as well as the "String" and "Double" items definition list (STRING_COLUMN、DOUBLE_COLUMN), we store the items in different list due to their types (Line 126-130).
  Put the two lists into one Datum unit and add arguments for each items in the lists, as done by the private method [makeDatum](Line 134).

  In the [makeDatum], we will store the data items into the string-list and double-list, which are in the format of TupleStringString and TupleStringDouble (Line 157-72).
  At first, we generate the string_values and num_values lists, as the factors required in a Datum class (Line 155-156).
  Then, we combine the corresponding items in "STRING_COLUMN" and "strList" as key-value pairs to generate the TupleStringString list (Line 158-161). And combine the corresponding items in "Double_COLUMN" and "doubleList" as key-value pairs to generate the TupleStringDouble list. Note that, because the data in doublelist is in String format, data convertion is required when put it into Datum unit (Line 167).
  
  Now, our learning data is ready in the Datum format.

  
 3. Model training (update learning model)

  Input the training data generated in step.2 into the add() method of AnomalyClient (Line 136).
  The first parameter in add() is the unique name for task identification in Zookeeper.
  (use null charactor "" for the stand-alone mode)
  The second parameter specifies the Datum generated in step.2.
  The returned result <string, float> is consisted of the data ID and its estimated anomaly value.
  
 4. Display result

  Display the returned value from add() method after a correction checking (Line 139).
  The anomaly value should not be infinity or　1.0　(Line 138).

-------------------------------------
Run the sample program
-------------------------------------

**［At Jubatus Server］**
 start "jubaanomaly" process.

::
 
  $ jubaanomaly --configpath config.json


**［At Jubatus Client］**
 Get the required package and Java client ready.
 Run!

 
**［Result］**

::

 ('574', 0.99721104) normal.
 ('697', 1.4958459) normal.
 ('1127', 0.79527026) normal.
 ('1148', 1.1487594) normal.
 ('1149', 1.2) normal.
 ('2382', 0.9994011) normal.
 ('2553', 1.2638165) normal.
 ('2985', 1.4081864) normal.
 ('3547', 1.275244) normal.
 ('3557', 0.90432936) normal.
 ('3572', 0.75777346) normal.
 ('3806', 0.9943142) normal.
 ('3816', 1.0017062) normal.
 ('3906', 0.5671135) normal.
 …
 …(omitted)

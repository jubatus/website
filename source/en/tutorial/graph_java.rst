Java
==================

Here we explain the sample program of Graph in Java. 

--------------------------------
Source_code
--------------------------------

In this sample program, we will explain 1) how to configure the learning-algorithms that used by Jubatus, with the example file 'train_route.json'; 2) how to learn the training data and calculate the shortest path with the example file ‘SearchRoute.java’. Here are the source codes of 'train_route.json' and 'SearchRoute.java'. 

**train_route.json**

.. code-block:: python

 1 : {
 2 :   "method": "graph_wo_index",
 3 :   "parameter": {
 4 :     "damping_factor" : 0.9,
 5 :     "landmark_num" : 256
 6 :   }
 7 : }
 

**CreateGraph.java**

.. code-block:: java

 001 : import java.io.InputStream;
 002 : import java.net.Authenticator;
 003 : import java.net.HttpURLConnection;
 004 : import java.net.PasswordAuthentication;
 005 : import java.net.URL;
 006 : import java.util.ArrayList;
 007 : import java.util.Collections;
 008 : import java.util.Comparator;
 009 : import java.util.HashMap;
 010 : import java.util.List;
 011 : import java.util.Map;
 012 : import javax.xml.parsers.DocumentBuilder;
 013 : import javax.xml.parsers.DocumentBuilderFactory;
 014 : import org.w3c.dom.Document;
 015 : import org.w3c.dom.Node;
 016 : import us.jubat.graph.Edge;
 017 : import us.jubat.graph.GraphClient;
 018 : import us.jubat.graph.PresetQuery;
 
 019 : public class CreateGraph {
 020 : 	public static final String HOST = "127.0.0.1";
 021 : 	public static final int PORT = 9199;
 022 : 	public static final String NAME = "trainRoute";
 
 023 : 	public Map<String, String> stations = new HashMap<String, String>();
 
 024 : 	private class StationJoin {
 025 : 		public String station1;
 026 : 		public String station2;
 
 027 : 		public StationJoin(String station1, String station2) {
 028 : 			this.station1 = station1;
 029 : 			this.station2 = station2;
 030 : 		}
 031 : 	}
 
 032 : 	private final void start() throws Exception {
 033 : 		// 1. Connect to Jubatus Server
 034 : 		GraphClient client = new GraphClient(HOST, PORT, 5);
 
 035 : 		// 2. Regist the preset query
 036 : 		PresetQuery pq = new PresetQuery();
 037 : 		pq.edge_query = new ArrayList<>();
 038 : 		pq.node_query = new ArrayList<>();
 039 : 		client.add_shortest_path_query(NAME, pq);
 
 040 : 		// 3. Generate the graph
 041 : 		this.createGraph(client, this.getStationJoin(11302)); // Yamanote Line
 042 : 		this.createGraph(client, this.getStationJoin(11312)); // Chuou Line
 
 043 : 		// 4. Show the Station IDs
 044 : 		System.out.println("=== Station IDs ===");
 045 : 		List<Map.Entry> entries = new ArrayList<Map.Entry>(stations.entrySet());
 046 : 		Collections.sort(entries, new Comparator() {
 047 : 			@Override
 048 : 			public int compare(Object o1, Object o2) {
 049 : 				Map.Entry e1 = (Map.Entry) o1;
 050 : 				Map.Entry e2 = (Map.Entry) o2;
 051 : 				return (Integer.valueOf((String) e1.getValue())).compareTo(Integer.valueOf((String) e2.getValue()));
 052 : 			}
 053 : 		});
 054 : 		for (Map.Entry e : entries) {
 055 : 			System.out.println(e.getValue() + "\t: " + e.getKey());
 056 : 		}
 057 : 	}
 
 058 : 	// Generate the combination list of 2 stations
 059 : 	private List<StationJoin> getStationJoin(int lineCd) throws Exception {
 060 : 		// Return list
 061 : 		List<StationJoin> joinList = new ArrayList<StationJoin>();
 
 062 : 		// Read the XML file
 063 : 		Document document = this.getXml(lineCd);
 
 064 : 		// Repeat for the number of <station_join> tags in XML file
 065 : 		for (int i = 0; i < document.getElementsByTagName("station_join").getLength(); i++) {
 066 : 			String station1 = "";
 067 : 			String station2 = "";
 068 : 			// Repeat for the number of childnodes surrounded by the <station_join> tags
 069 : 			for (int j = 0; j < document.getElementsByTagName("station_join").item(i).getChildNodes().getLength(); j++) {
 070 : 				Node node = document.getElementsByTagName("station_join").item(i).getChildNodes().item(j);
 071 : 				String nodeName = node.getNodeName();
 072 : 				String nodeValue = null;
 073 : 				// Get the values of station_name1 and station_name2
 074 : 				if (node.getFirstChild() != null) {
 075 : 					nodeValue = node.getFirstChild().getNodeValue();
 076 : 				}
 077 : 				if (nodeName == "station_name1") {
 078 : 					station1 = nodeValue;
 079 : 				} else if (nodeName == "station_name2") {
 080 : 					station2 = nodeValue;
 081 : 				}
 082 : 			}
 083 : 			joinList.add(new StationJoin(station1, station2));
 084 : 		}
 085 : 		return joinList;
 086 : 	}
 
 087 : 	// Read the XML file
 088 : 	private Document getXml(int lineCd) throws Exception {
 089 : 		// Set the proxy 
 090 : 		System.setProperty("proxySet", "true");
 091 : 		System.setProperty("proxyHost", "192.168.00.0");
 092 : 		System.setProperty("proxyPort", "8080");
 
 093 : 		// Set the BASIC certification
 094 : 		final String username = "user";
 095 : 		final String password = "password";
 096 : 		Authenticator.setDefault(new Authenticator() {
 097 : 			@Override
 098 : 			protected PasswordAuthentication getPasswordAuthentication() {
 099 : 				return new PasswordAuthentication(username, password.toCharArray());
 100 : 			}
 101 : 		});
 
 102 : 		// Read the XML file from WEB
 103 : 		String urlStr = "http://www.ekidata.jp/api/n/" + String.valueOf(lineCd) + ".xml";
 104 : 		URL url = new URL(urlStr);
 105 : 		HttpURLConnection connection = (HttpURLConnection) url.openConnection();
 106 : 		connection.setDoOutput(true);
 107 : 		connection.setUseCaches(false);
 108 : 		connection.setRequestMethod("GET");
 109 : 		InputStream inputStream = connection.getInputStream();
 110 : 		DocumentBuilder docBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
 111 : 		Document document = docBuilder.parse(inputStream);
 
 112 : 		return document;
 113 : 	}
 
 114 : 	// 3. Generate the Graph
 115 : 	private void createGraph(GraphClient client, List<StationJoin> stationJoin) {
 116 : 		// Repeat for the number of two-stations' combination lists that got from XML list
 117 : 		for (StationJoin join : stationJoin) {
 118 : 			// 3-1. Get the station information and ID
 119 : 			String s1_node_id = this.addStation(client, join.station1);
 120 : 			String s2_node_id = this.addStation(client, join.station2);
 
 121 : 			// 3-2. Make bi-links between new added two stations
 122 : 			Edge edge1 = new Edge();
 123 : 			edge1.property = new HashMap<>();
 124 : 			edge1.source = s1_node_id;
 125 : 			edge1.target = s2_node_id;
 126 : 			Edge edge2 = new Edge();
 127 : 			edge2.property = new HashMap<>();
 128 : 			edge2.source = s2_node_id;
 129 : 			edge2.target = s1_node_id;
 130 : 			client.create_edge(NAME, s1_node_id, edge1);
 131 : 			client.create_edge(NAME, s2_node_id, edge2);
 
 132 : 			client.update_index(NAME);
 133 : 		}
 134 : 	}
 
 135 : 	private String addStation(GraphClient client, String station) {
 136 : 		String nodeId;
 137 : 		Map<String, String> property = new HashMap<String, String>();
 138 : 		// Check whether the 'station', as the argument, has be stored in the Map or not.
 139 : 		if (this.stations.containsKey(station)) {
 140 : 			// If yes, return the ID
 141 : 			nodeId = this.stations.get(station);
 142 : 		} else {
 143 : 			// If no, create a new node for the station, and return its ID.
 144 : 			nodeId = client.create_node(NAME);
 145 : 			property.put("name", station);
 146 : 			client.update_node(NAME, nodeId, property);
 147 : 			// Store the created node into the Map of stations
 148 : 			this.stations.put(station, nodeId);
 149 : 		}
 150 : 		return nodeId;
 151 : 	}
 
 152 : 	public static void main(String[] args) throws Exception {
 153 : 		new CreateGraph().start();
 154 : 		System.exit(0);
 155 : 	}
 156 : }
 
 
**SearchRoute.java**

.. code-block:: java

 01 : import java.util.ArrayList;
 02 : import java.util.List;
 03 : import us.jubat.graph.GraphClient;
 04 : import us.jubat.graph.Node;
 05 : import us.jubat.graph.PresetQuery;
 06 : import us.jubat.graph.ShortestPathQuery;
 
 07 : public class SearchRoute {
 08 : 	public static final String HOST = "127.0.0.1";
 09 : 	public static final int PORT = 9199;
 10 : 	public static final String NAME = "trainRoute";
 
 11 : 	private final void start(String source, String target) throws Exception {
 12 : 		// 1. Connect to Jubatus Server
 13 : 		GraphClient client = new GraphClient(HOST, PORT, 5);
 
 14 : 		// 2. Prepare the query
 15 : 		PresetQuery pq = new PresetQuery();
 16 : 		pq.edge_query = new ArrayList<>();
 17 : 		pq.node_query = new ArrayList<>();
 
 18 : 		ShortestPathQuery query = new ShortestPathQuery();
 19 : 		query.source = source;
 20 : 		query.target = target;
 21 : 		query.max_hop = 100;
 22 : 		query.query = pq;
 
 23 : 		// 3. Calculate the shortest path
 24 : 		List<String> stations = client.get_shortest_path(NAME, query);
 
 25 : 		// 4. Return the results
 26 : 		System.out.println("Pseudo-Shortest Path (hops) from " + query.source + "to " + query.target);
 27 : 		for (String station : stations) {
 28 : 			Node node = client.get_node(NAME, station);
 29 : 			String stationName = "";
 30 : 			if (node.property.containsKey("name")) {
 31 : 				stationName = node.property.get("name");
 32 : 			}
 33 : 			System.out.println(station + "\t: " + stationName);
 34 : 		}
 35 : 	}
 
 36 : 	public static void main(String[] args) throws Exception {
 37 : 		new SearchRoute().start(args[0], args[1]);
 38 : 		System.exit(0);
 39 : 	}
 
 40 : }


--------------------------------
Explanation
--------------------------------

**train_route.json**

The configuration information is given by the JSON unit. Here is the meaning of each JSON filed.

 * method
 
  Specify the algorithm used in graph mining. In this example, we use the graph without indexing, so we specify it with "graph_wo_index".
  
 * parameter
 
  Specify the parameters to be passed to the algorithm.
  We specify two parameter here, "damping_factor" and "landmark_num".
  "damping_factor" is the damping factor used in PageRank calculation. It adjusts scores for nodes with differenct degrees.The bigger it is, the more sensitive to graph structure PageRank score is, but the larger biases it causes. In the original paper, 0.85 is good.
  "landmark_num" is used for shortest path calculation. The bigger it is, more accurate value you can get, but the more memory is required. 


**CreateGraph.java**

 CreateGraph.java generates a graph composed of Yamanote-line and Chuou-line. The client program in Graph will use the 'GraphClient' class defined in 'us.jubat.graph'. Here are the 5 methods used in the sample.
 
 * add_shortest_path_query(String name, PresetQuery query)
 
  Regist the shortest-path calculation query that to be used.

 * create_node(String name)
 
  Add one node into graph.

 * update_node(String name, String node_id, Map<String, String> property)
 
  Update a node's 'node_id' attribute in property map.

 * create_edge(String name, String node_id, Edge e)
 
  Make the link from e.source to e.target.

 * get_shortest_path(String name, ShortestPathQuery query)
 
  Calculates (from the precomputed data) a shortest path from query.source to query.target that matches the preset query.

 1. Connect to Jubatus Server

  Connect to Jubatus Server (Line 34).
  Setting the IP addr., RPC port of Jubatus Server, and the connection waiting time.

 2. Regist the preset query
  
  The 'add_shortest_path_query' method must be registered beforehand. Therefore, the 'PresetQuery' is made (Line 36), and its pq.edge_query and pq.node_query are filled with the newly declared ArrayList (Line 37, 38). Finally, the query made by 'add_shortest_path_query' is registed (Line 39).

 3. Generate the graph

  Make the graph composed of Yamanote-line and Chuou-line.
  Firstly, private method [createGraph] is called at (Line 41, 42).
  The first parameter in [createGraph] is the GraphClient made in Step. 1. 
  The second prarmeter is the return value from private method [getStationJoin].
  
  Private method [getStationJoin] makes the combination list of two neighbor stations.
  At first, the ArrayList of inner class [StationJoin] is made (Line 27).
  Then, set the instance variable, station1 and station2, in [StationJoin] Class (Line 28-29).
  After setting the two stations' name, method [getStationJoin] will make the combination list.
  
  Next, we get the station information from the Web. Private method [getXml] is called to download the XML file (Line 61).
  The same parameter is passed from [getStationJoin] to [getXml] method.
  This parameter is used to make the URL, from which to download XML file.
  Proxy for the private method [getXml] is set in (Line 87-92). Please comment out them if not needed.
  Codes in (Line 102-111) are the processes for reading the XML file.
  Contents of the XML file likes below.
  In this sample program, we ignore the factor of 'distance', and only consider the connections between stations. So, the values in <station_name1>, <station_name2> are not used in the program.  
  ::
  
   <ekidata version="ekidata.jp station_join api 1.0">
   <station_join>
    <station_cd1>1131231</station_cd1>
    <station_cd2>1131232</station_cd2>
    <station_name1>Nichi-Hachioji</station_name1>
    <station_name2>Takao</station_name2>
    <lat1>35.656621</lat1>
    <lon1>139.31264</lon1>
    <lat2>35.642026</lat2>
    <lon2>139.282288</lon2>
   </station_join>
   <station_join>
    <station_cd1>1131230</station_cd1>
    <station_cd2>1131231</station_cd2>
    <station_name1>Hachioji</station_name1>
    <station_name2>Nichi-Hachioji</station_name2>
    <lat1>35.655555</lat1>
    <lon1>139.338998</lon1>
    <lat2>35.656621</lat2>
    <lon2>139.31264</lon2>
   </station_join>
   <station_join>
    <station_cd1>1131229</station_cd1>
    <station_cd2>1131230</station_cd2>
    <station_name1>Toyota</station_name1>
    <station_name2>Hachioji</station_name2>
    <lat1>35.659502</lat1>
    <lon1>139.381495</lon1>
    <lat2>35.655555</lat2>
    <lon2>139.338998</lon2>
   </station_join>
   -Snip-
   

  Now, we input the value of <station_cd1> in the XML file into the instance variable 'station1' in [StationJoin] class, and the value of <station_cd2> in to 'station2'.
  The number of instance created in [StationJoin] is the same as the number of <station_join> tags, and they are sotred in the ArrayList that created at Line 41 （Line 65-85).
  
  Next, we make the graph by using the ArrayList<StationJoin> created above (Line 114-134).
  The private method [createGraph] performs the following task.
  
   3-1. Add station information and ID.
    Insert node into graph. Here, a node means a station. (eg. Shinagawa, Ochanomizu, Tokyo, etc.)
    
   3-2. Create links between the added two neighbor stations
    Make the bi-link between the registed station to its neighbor stations. Here, a link means a route. (eg. Harajuku <-> Shibuya, etc.)
    
  3-1. Add station information and ID.
   Private method [addStation] is called (Line 119-120), to add every pair of neighboring nodes <station1, station2> in to the graph. 
   Method [addStation] will check the instance variable 'stations' (of HashMap<String, String> type). If the HashMap contains the specified station, the station_id will be returned; Otherwise, a new node is created, and its ID is returned after storing the nodeID and station name into the 'stations' Hashmap (Line 143-138).
   Mehods [create_node] and [update_node] in GraphClient regist the new node (Line 144-146).
   At first, [create_node] method is called with its argument set by an unique task name in the ZooKeeper cluster, and the returned value is the nodeId (Line 144).
   After that, a node is added into the graph. Then, we regist the key-value <name, "station name"> into the 'property' (Line 148), which is the instance of HashMap<String, String> created at Line 137.
   Finally, [update_node] method updates the 'property' with the node created at Line 144 (Line 146).
   
  3-2. Create links between the added two neighbor stations
   After adding the two neighbor stations by method [addStation], we create the bi-links between station1 and station2 (Line 121-131).
   Method [create_edge] is used to create the bi-links.
   The second argument means the start node's ID. The third argument is an instance of Edge class, which stores the nodeID of both start and end nodes in the edge.
   
  The [update_index] method in Line 132 is used for locally Mix operation, do not use it in distributed environment.
  
 4. Show the stations

  In step 3-1, station name and station ID(nodeID) are stored into the "stations". Here, we output the stations names by the ascending order of their IDs (Line 46-56).
  
 **SearchRoute.java**
 
 SearchRoute.java finds the shortest path between every 2 stations from the graph that made by CreateGraph.java.
 The method it used is the "get_shortest_path".
  
  1. Connect to Jubatus Server

   Connect to Jubatus Server (Line 13).
   Setting the IP addr., RPC port of Jubatus Server, and the connection waiting time.

   
  2. Prepare the query

   Prepare the query for the shortest path calculation (Line 14-22).
   Create the ShortestPathQuery required by the [get_shortest_path] method (Line 18).
   Store the start node's & end node's nodeIDs into the source & target variables in the 'ShortestPathQuery'. 
   The process will be truncated if it fails to find the route within the specified number of 'maxhop'.
   Also note, the query should be registed by "add_shortest_path_query" beforehand.
   
  3. Calculate the shortes path

   By specifying the "ShortestPathQuery" that created in Step.2, get_shortest_path(String name, ShortestPathQuery query)method will find the shortest path (Line 24). It calculates (from the precomputed data) the shortest path from query.source to query.target that matches the preset query. 
   
  4. Show the results

   Show the ID of stations that on the shortes path calculated in Step 3 (Line 26-34).


-------------------------------------
Run the sample program
-------------------------------------

［At Jubatus Server］
 start "jubagraph" process.
 
 ::
 
  $ jubagraph --configpath train_route.json
 

［At Jubatus Client］
 Get the required package and Java client ready.
 Run create_graph.java!
 
 ::
 
  $ java CreateGraph
  
  === Station IDs ===
  0       Shinagawa
  1       Osaki
  4       Tamachi
  ...
  139     Nagano
  144     Yotsuya
  147     Ochanomizu
  
 Output of the station name, and their station ID (node ID on graph).

 Search the shortest path between 2 stations.
 
 ::
 
  $ java SearchRoute 0 144
  
  Pseudo-Shortest Path (hops) from 0 to 144:
  0     Shinagawa
  4     Tamachi
  7     Hamamatsucho
  10    Shinbashi
  13    Yurakucho
  16    Tokyo
  19    Kanda
  147   Ochanomizu
  144   Yotsuya


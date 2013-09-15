Nearest Neighbor
================

* See `IDL definition <https://github.com/jubatus/jubatus/blob/master/jubatus/server/server/nearest_neighbor.idl>`_ for detailed specification.
* See :doc:`method` for detailed description of algorithms used in this server.


Configuration
~~~~~~~~~~~~~

Configuration is given as a JSON file.
We show each filed below:

.. describe:: method

   Specify algorithm for nearest neighbor.
   You can use these algorithms.

   .. table::

      ==================== ===============================================================
      Value                Method
      ==================== ===============================================================
      ``"lsh"``            Use Locality Sensitive Hashing based on cosine similarity.
      ``"minhash"``        Use MinHash. [Ping2010]_
      ``"euclid_lsh"``     Use LSH based on cosine similarity for nearest neighbor search with Euclidean distance.
      ==================== ===============================================================


.. describe:: parameter

   Specify parameters for the algorithm.
   Its format differs for each ``method``.

   lsh
     :bitnum:
        Bit length of hash values.
        The bigger it is, the more accurate results you can get, but the more memory is required.
        (Integer)

   minhash
     :bitnum:
        Number of hash values.
        The bigger it is, the more accurate results you can get, but the more memory is required.
        (Integer)

   euclid_lsh
     :hash_num:
        Number of hash values.
        The bigger it is, the more accurate results you can get, but the fewer results you can find and the more memory is required.
        (Integer)

.. describe:: converter

   Specify configuration for data conversion.
   Its format is described in :doc:`fv_convert`.


Example:
  .. code-block:: javascript

     {
       "method": "lsh",
       "parameter" : {
         "bit_num" : 64
       },
       "converter" : {
         "string_filter_types": {},
         "string_filter_rules":[],
         "num_filter_types": {},
         "num_filter_rules": [],
         "string_types": {},
         "string_rules":[
           {"key" : "*", "type" : "str", "sample_weight":"bin", "global_weight" : "bin"}
         ],
         "num_types": {},
         "num_rules": [
           {"key" : "*", "type" : "num"}
         ]
       }
     }


Data Structures
~~~~~~~~~~~~~~~

.. mpidl:type:: neighbor_result

   Represents a result of nearest neighbor methods.
   It is a list of tuple of string and float.
   The string value is a row ID and the float value is a similarity or distance for the ID.
   It depend on the API if the float value represents similarity or distance.
   If the float value is a similarity value, higher value means higher similarity with the query of the row ID.
   Otherwise, smaller value means closer distance with the query of the row ID.

   .. code-block:: c++

      type neighbor_result = list<tuple<string, float> >


Methods
~~~~~~~

For all methods, the first parameter of each method (``name``) is a string value to uniquely identify a task in the ZooKeeper cluster.
When using standalone mode, this must be left blank (``""``).


.. mpidl:service:: nearest_neighbor

   .. mpidl:method:: bool init_table(0: string name)

      TODO

   .. mpidl:method:: bool set_row(0: string name, 1: string id, 2: datum d)

      :param name: string value to uniquely identifies a task in the ZooKeeper cluster
      :param id:   row ID
      :param row:  :mpidl:type:`datum` for the row
      :return:     True if this function updates models successfully

      Updates the row whose id is ``id`` with given ``row``.
      If the row with the same ``id`` already exists, the row is differential updated with ``row``.
      Otherwise, new row entry will be created.
      If the server that manages the row and the server that received this RPC request are same, this operation is reflected instantly.
      If not, update operation is reflected after mix.

   .. mpidl:method:: neighbor_result neighbor_row_from_id(0: string name, 1: string id, 2: uint size)

      :param name: string value to uniquely identifies a task in the ZooKeeper cluster
      :param id:  row ID in the nearest neighbor search table
      :param size: number of rows to be returned
      :return:     row IDs that are the nearest to the row ``id`` and their /distance values

      Returns ``size`` rows (at maximum) that have most similar :mpidl:type:`datum` to ``id`` and their distance values.

   .. mpidl:method:: neighbor_result neighbor_row_from_data(0: string name, 1: datum query, 2: uint size)

      :param name: string value to uniquely identifies a task in the ZooKeeper cluster
      :param query: :mpidl:type:`datum` for nearest neighbor search
      :param size: number of rows to be returned
      :return:     row IDs that are the nearest to ``query`` and their distance values

      Returns ``size`` rows (at maximum) of which :mpidl:type:`datum` are most similar to ``query`` and their distance values.
                   
   .. mpidl:method:: neighbor_result similar_row_from_id(0: string name, 1: string id, 2: int ret_num)


      :param name: string value to uniquely identifies a task in the ZooKeeper cluster
      :param id:  row ID in the nearest neighbor search table
      :param ret_num: number of rows to be returned
      :return:     row IDs that are the nearest to the row ``id`` and their similarity values

      Returns ``ret_num`` rows (at maximum) that have most similar :mpidl:type:`datum` to ``id`` and their similarity values.

   .. mpidl:method:: neighbor_result similar_row_from_data(0: string name, 1: datum query, 2: int ret_num)

      :param name: string value to uniquely identifies a task in the ZooKeeper cluster
      :param query: :mpidl:type:`datum` for nearest neighbor search
      :param ret_num: number of rows to be returned
      :return:     row IDs that are the nearest to ``query`` and their similarity values

      Returns ``ret_num`` rows (at maximum) of which :mpidl:type:`datum` are most similar to ``query`` and their similarity values.

jubatus::client::graph
----------------------

See `IDL definition <https://github.com/jubatus/jubatus/blob/master/src/server/graph.idl>`_ for original and detailed spec.

typedef
~~~~~~~

.. code-block:: c++

  type centrality_type = int
  type node_id = string
  type edge_id_t = ulong

  type property = map<string, string> 

  message node_info {
    0: property p
    1: list<edge_id_t>  in_edges
    2: list<edge_id_t>  out_edges
  }

  message preset_query {
    0: list<tuple<string, string> > edge_query
    1: list<tuple<string, string> > node_query
  }

  message edge_info {
    0: property p
    1: node_id src
    2: node_id tgt
  }

  message shortest_path_req {
    0: node_id src
    1: node_id tgt
    2: uint max_hop
    3: preset_query q
  }


graph methods
~~~~~~~~~~~~~

.. describe:: string create_node(0: string name)

.. describe:: int remove_node(0: string name, 1: string nid)

.. describe:: int update_node(0: string name, 1: string nid, 2: property p)

.. describe:: int create_edge(0: string name, 1: string nid, 2: edge_info ei)

.. describe:: int update_edge(0: string name, 1: string nid, 2: edge_id_t eid, 3: edge_info ei)

.. describe:: int remove_edge(0: string name, 1: string nid, 2: edge_id_t e)

.. describe:: double centrality(0: string name, 1: string nid, 2: centrality_type ct, 3: preset_query q)


.. describe:: bool add_centrality_query(0: string name, 1: preset_query q)

.. describe:: bool add_shortest_path_query(0: string name, 1: preset_query q)

.. describe:: bool remove_centrality_query(0: string name, 1: preset_query q)

.. describe:: bool remove_shortest_path_query(0: string name, 1: preset_query q)

.. describe:: list<node_id>  shortest_path(0: string name, 1: shortest_path_req r)

.. describe:: int update_index(0: string name)

.. describe:: int clear(0: string name)

.. describe:: node_info get_node(0: string name, 1: string nid)

.. describe:: edge_info get_edge(0: string name, 1: string nid, 2: edge_id_t e)

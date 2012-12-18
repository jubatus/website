Anomaly
-------

* See `IDL definition <https://github.com/jubatus/jubatus/blob/master/src/server/anomaly.idl>`_ for detailed specification.

Data Structures
~~~~~~~~~~~~~~~

None.

Methods
~~~~~~~

For all methods, the first parameter of each method (``name``) is a string value to uniquely identify a task in the ZooKeeper cluster.
When using standalone mode, this must be left blank (``""``).

.. describe:: bool clear_row(string name, string id)

 - Parameters:

  - ``name`` : string value to uniquely identifies a task in the ZooKeeper cluster
  - ``id`` : point ID to be removed

 - Returns:

  - True when the point was cleared successfully

 Clears a point data with ID ``id``.

.. describe:: tuple<string, float> add(0: string name, 1: datum d)

 - Parameters:

  - ``name`` : string value to uniquely identifies a task in the ZooKeeper cluster
  - ``d`` : datum

 - Returns:

  - Tuple of the point ID and the anomaly measure value

 Adds a point data ``d``.

.. describe:: float update(0: string name, 1: string id, 2: datum d)

 - Parameters:

  - ``name`` : string value to uniquely identifies a task in the ZooKeeper cluster
  - ``id`` : point ID to update
  - ``d`` : new value for the point

 - Returns:

  - Anomaly measure value

 Updates the point ``id`` with the given datum ``d``.

.. describe:: bool clear(0: string name)

 - Parameters:

  - ``name`` : string value to uniquely identifies a task in the ZooKeeper cluster

 - Returns:

  - True when the model was cleared successfully

 Completely clears the model.

.. describe:: float calc_score(0: string name, 1: datum d)

 - Parameters:

  - ``name`` : string value to uniquely identifies a task in the ZooKeeper cluster
  - ``d`` : datum

 - Returns:

  - Anomaly measure value

 Calculates an anomaly measure value for datum ``d`` without adding a point.

.. describe:: list<string> get_all_rows(0:string name)

 - Parameters:

  - ``name`` : string value to uniquely identifies a task in the ZooKeeper cluster

 - Returns:

  - list of all point IDs

 Returns the list of all point IDs.

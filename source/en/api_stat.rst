jubatus::client::stat
===============================

typedef
--------

jubatus::stat::config_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++

   struct config_data {
     int32_t window_size;
   };


constructor
-----------------

.. cpp:function:: stat(const string& hosts, const string& name, double timeout)

 - Parameters:

   - ``hosts`` : servers and numbers of ports of jubakeepers. Format of this option must be  ``ipaddress:port,hostname:port,...`` . 
   - ``name``  : a string value to uniquely identifies a task in Zookeeper quorum
   - ``timeout`` : connection timeout for RPC

Constructor of stat.


stat methods
---------------------

<FILLME>

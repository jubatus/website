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

- ``hosts`` : jubakeeperのサーバ、ポートを指定。書式は、 ``ipaddress:port,hostname:port,...`` の形式に従うこと。
- ``name`` :  ZooKeeperクラスタが学習器を一意に識別する値
- ``timeout`` : 通信時のタイムアウトまでの時間を指定


stat methods
---------------------

<FILLME>

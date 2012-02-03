jubatus::client::regression
===============================

typedef
--------

jubatus::regression::config_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++

   struct config_data {
     std::string method;
     jubatus::converter_config converter;
   };



jubatus::regression::estimate_result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++

   typedef float estimate_rusult;
   typedef std::vector<estimate_result> estimate_results;




constructor
-----------------

.. cpp:function:: regression(const string& hosts, const string& name, double timeout)

- ``hosts`` : jubakeeperのサーバ、ポートを指定。書式は、 ``ipaddress:port,hostname:port,...`` の形式に従うこと。
- ``name`` :  ZooKeeperクラスタが学習器を一意に識別する値
- ``timeout`` : 通信時のタイムアウトまでの時間を指定


common methods
-----------------

.. cpp:function:: void regression::save(const string& type, const string& id)

typeとidを指定して **すべての** サーバのローカルディスクに、それぞれのサーバが学習したモデルを保存する。


.. cpp:function:: void regression::load(const string& type, const string& id)

typeとidを指定して **すべての** サーバのローカルディスクから、それぞれのサーバが学習したモデルをロードする。


.. cpp:function:: void regression::set_config(const config_data& config)

**すべての** サーバーのコンフィグを更新する。


.. cpp:function:: config_data regression::get_config()

コンフィグを取得する。

.. cpp:function:: std::map<std::pair<std::string, int>, std::map<std::string, std::string> > client::get_status()

**すべての** サーバーの状態を取得する。
各サーバーは、ホスト名とポートのペアで表される。それぞれのサーバーに関して、内部状態を文字列から文字列へのマップで状態を返す。



regression methods
---------------------

.. cpp:function:: void regression::train(const std::vector<std::pair<float, datum> >& data)

ランダムにひとつ選んだサーバーで学習を行う。 ``std::pair<float, datum>`` は、あるdatumとそれに対する値の組み合わせである。これをvectorとして、一度で複数のdatumと値の組を学習させる。


.. cpp:function:: std::vector<regression::estimate_result> regression::estimate(const std::vector<datum>& data)

ランダムにひとつ選んだサーバーで学習を行う。 複数のdatumを一度に渡すことができる。引数のdatumと戻り値のestimate_resultは、vectorのオフセットで1:1に対応している。 ``estimate_result`` 
は回帰の結果を返す。


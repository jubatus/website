jubatus::client::recommender
===============================

typedef
--------

jubatus::recommender::config_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++

   struct config_data {
     jubatus::converter_config converter;
     std::string similarity_name;
     std::string anchor_finder_name;
     std::string anchor_builder_name;
     size_t all_anchor_num;
     size_t anchor_num_per_data;
   };



jubatus::recommend::estimate_result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++

    typedef std::vector<std::pair<std::string, float> > similar_result;
    typedef std::vector<std::pair<std::string, datum> > rows;



constructor
-----------------

.. cpp:function:: recommender(const string& hosts, const string& name, double timeout)

- ``hosts`` : jubakeeperのサーバ、ポートを指定。書式は、 ``ipaddress:port,hostname:port,...`` の形式に従うこと。
- ``name`` :  ZooKeeperクラスタが学習器を一意に識別する値
- ``timeout`` : 通信時のタイムアウトまでの時間を指定


common methods
-----------------

.. cpp:function:: void recommender::save(const string& type, const string& id)

typeとidを指定して **すべての** サーバのローカルディスクに、それぞれのサーバが学習したモデルを保存する。


.. cpp:function:: void recommender::load(const string& type, const string& id)

typeとidを指定して **すべての** サーバのローカルディスクから、それぞれのサーバが学習したモデルをロードする。


.. cpp:function:: void recommender::set_config(const config_data& config)

**すべての** サーバーのコンフィグを更新する。


.. cpp:function:: config_data recommender::get_config()

コンフィグを取得する。

.. cpp:function:: std::map<std::pair<std::string, int>, std::map<std::string, std::string> > client::get_status()

**すべての** サーバーの状態を取得する。
各サーバーは、ホスト名とポートのペアで表される。それぞれのサーバーに関して、内部状態を文字列から文字列へのマップで状態を返す。



regression methods
---------------------

.. cpp:function:: void update_row(const jubatus::recommender::rows& dat);

<FIXME>ランダムにひとつ選んだサーバーに対して、jubatus::recommender::rowsで表される行を追加する。

.. cpp:function:: void clear_row(const std::vector<std::string>& ids);

すべてのサーバに対して、idsで表されるrowを削除する。

.. cpp:function:: void build(); 

recommenderをbuildする。build() is only for standalone mode

.. cpp:function:: datum complete_row_from_id(const std::string& id);

指定したidのrowの中で欠けている値を予測して返す。

.. cpp:function:: datum complete_row_from_data(const datum& dat);

指定したdatumで構成されるrowの中で欠けている値を予測して返す。

.. cpp:function:: jubatus::recommender::similar_result similar_row_from_id(const std::string& id, size_t ret_num);

指定したidに近いrowを返す。

.. cpp:function:: jubatus::recommender::similar_result similar_row_from_data(const datum& dat, size_t ret_num);

指定したdatumで構成されるrowに近いrowを返す。

.. cpp:function:: datum decode_row(const std::string& id);

<FIXME>

.. cpp:function:: jubatus::recommender::rows get_all_rows();

すべてのrowを返す。



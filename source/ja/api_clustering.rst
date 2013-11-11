Clustering
----------

* 詳細な仕様は `IDL 定義 <https://github.com/jubatus/jubatus/blob/master/jubatus/server/server/clustering.idl>`_ と、
  `分析用サーバのIDL 定義 <https://github.com/jubatus/jubatus/blob/master/jubatus/server/server/cluster_analysisidl>`_ を参照してください。


Configuration
~~~~~~~~~~~~~

設定は単体の JSON で与えられる。
JSON の各フィールドは以下のとおりである。

.. describe:: method

   クラスタリングに使用するアルゴリズムを指定する。
   以下のアルゴリズムを指定できる。

   .. table::

      ==================== ===================================
      設定値               手法
      ==================== ===================================
      ``"kmeans"``         k-meansを利用する
      ``"gmm"``            ガウス混合モデルを利用する
      ==================== ===================================

.. describe:: parameter

   アルゴリズムに渡すパラーメータを指定する。
 
   :k:
     いくつのクラスタに分割するか、を指定する。
     (Integer)

   :compressor_method:
     点を圧縮するアルゴリズムを指定する．
     ``simple``, ``compressive_kmeans``, ``compressice_gmm`` から選ぶことができる。

   :backet_size:
     一度に圧縮する点数．ここではデータセットのサイズに等しく設定する．
     (Integer)

   :backet_length:
     TBF
     (Integer)

   :compresed_backet_size:
     backet_sizeを何点に圧縮するか．
     この実験に於いては圧縮率=(compressed_backet_size/backet_size)である．
       (Integer)

   :bicriteria_base_size:
     圧縮の粗さに関係するパラメータ．
     (Integer)

   :forgetting_factor:
     TBF
     (double)

   :forgetting_threshold:
     TBF
     (double)

.. describe:: converter

   特徴変換の設定を指定する。
   フォーマットは :doc:`fv_convert` で説明する。


例:
  .. code-block:: javascript

     {
       "method" : "simple",
       "parameter" : {
         }
       },
       "converter" : {
         "string_filter_types" : {},
         "string_filter_rules" : [],
         "num_filter_types" : {},
         "num_filter_rules" : [],
         "string_types" : {},
         "string_rules" : [
           { "key" : "*", "type" : "str", "sample_weight" : "bin", "global_weight" : "bin" }
         ],
         "num_types" : {},
         "num_rules" : [
           { "key" : "*", "type" : "num" }
         ]
       }
     }


Data Structures
~~~~~~~~~~~~~~~

なし。


Methods
~~~~~~~

各メソッドの最初のパラメタ ``name`` は、タスクを識別する ZooKeeper クラスタ内でユニークな名前である。
スタンドアロン構成では、空文字列 (``""``) を指定する。

.. mpidl:service:: clustering

   .. mpidl:method:: bool push(0: string name, 1: list<datum> points)

      :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
      :points:     追加する点のリスト
      :return:     点の追加に成功した場合 True

      ID ``id`` で指定される点データを削除する。

   .. mpidl:method:: uint get_revision(0: string name)

      :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
      :return:     クラスタ状態のバージョン

      クラスタ状態のバージョンを返す．

   .. mpidl:method:: list<list<tuple<double, datum> > > get_core_members(0: string name)

      :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
      :return:     クラスタの概略

      クラスタのコアセットを返す。

   .. mpidl:method:: list<datum> get_k_center(0: string name)

      :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
      :return:     クラスタ中心

      ``k`` 個のクラスタ中心を返す．

   .. mpidl:method:: datum get_nearest_center(0: string name, 1: datum point)

      :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
      :param point:  :mpidl:type:`datum`
      :return:     与えられた点に最も近いクラスタ中心

      点を追加せずに、与えられた点データ ``point`` に最も近いクラスタ中心を返す．

   .. mpidl:method:: list<tuple<double, datum> > get_nearest_members(0: string name, 1: datum point)

      :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
      :param point: 指定する点
      :return:     点のリスト

      ``point`` で指定した点から最も近いクラスタの概略を返す。

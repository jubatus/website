Common Data Structures and Methods
----------------------------------

以下のデータ構造とメソッドは各サーバで利用可能である。

Data Structures
~~~~~~~~~~~~~~~

.. mpidl:message:: datum

   Jubatus で機械学習の対象となるデータを表す。
   詳細は :doc:`fv_convert` を参照すること。

   .. mpidl:member:: 0: list<tuple<string, string> > string_values

      文字列で表現される入力データである。
      データのキーと値のペアの集合として表現される。
      キーの名前に "$" 記号を含めることはできない。

   .. mpidl:member:: 1: list<tuple<string, double> > num_values

      数値で表現される入力データである。
      データのキーと値のペアの集合として表現される。

   .. code-block:: c++

      message datum {
        0: list<tuple<string, string> > string_values
        1: list<tuple<string, double> > num_values
      }


Constructor
~~~~~~~~~~~

.. describe:: constructor(string host, int port, int timeout_sec)

   新しい RPC クライアントのインスタンスを作成します。
   ``timeout_sec`` には RPC メソッドの実行からレスポンスまでのタイムアウト時間を指定します。

   現在、Python と Ruby クライアントでは ``timeout_sec`` を指定することができません。

   コンストラクタの利用方法を以下に示します:

.. code-block:: cpp

   // C++
   #include <jubatus/client.hpp>
   using jubatus::classifier::client::classifier;
   // ...
   classifier client("localhost", 9199, 10);

.. code-block:: python

   # Python
   from jubatus.classifier.client import classifier
   # ...
   client = classifier("localhost", 9199);

.. code-block:: ruby

   // Ruby
   require 'jubatus/classifier/client'
   include Jubatus::Classifier::Client
   // ...
   client = Classifier.new("localhost", 9199)

.. code-block:: java

   // Java
   import us.jubat.classifier.ClassifierClient;
   // ...
   ClassifierClient client = new ClassifierClient("localhost", 9199, 10);


Methods
~~~~~~~

各メソッドの最初のパラメタ ``name`` は、タスクを識別する ZooKeeper クラスタ内でユニークな名前である。
スタンドアロン構成では、空文字列 (``""``) を指定する。

.. mpidl:method:: bool save(0: string name, 1: string id)

   :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
   :param id:   保存されるファイル名
   :return:     すべてのサーバで保存が成功したらTrue

   **すべて** のサーバで学習モデルをローカルディスクに保存する。

.. mpidl:method:: bool load(0: string name, 1: string id)

   :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
   :param id:   読み出すファイル名
   :return:     すべてのサーバで読み出しに成功したらTrue

   **すべて** のサーバで、保存された学習モデルをローカルディスクから読み出す。

.. mpidl:method:: bool clear(0: string name)

   :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
   :return:     モデルの削除に成功した場合 True

   **すべて** のサーバで、モデルを完全に消去する。

.. mpidl:method:: string get_config(0: string name)

   :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
   :return:     初期化時に設定した設定情報

   サーバの設定を取得する。
   取得される設定情報内容については、各サービスの API リファレンスを参照のこと。

.. mpidl:method:: map<string, map<string, string> >  get_status(0: string name)

   :param name: タスクを識別する ZooKeeper クラスタ内でユニークな名前
   :return:     それぞれのサーバの内部状態。最上位の map のキーは ``ホスト名_ポート番号`` 形式である。

   **すべての** サーバの内部状態を取得する。
   サーバはホスト名、ポート番号で識別する。

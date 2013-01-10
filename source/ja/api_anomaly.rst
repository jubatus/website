Anomaly
-------

* 詳細な仕様は `IDL 定義 <https://github.com/jubatus/jubatus/blob/master/src/server/anomaly.idl>`_ を参照してください。

Data Structures
~~~~~~~~~~~~~~~

なし。

Methods
~~~~~~~

各メソッドの最初のパラメタ ``name`` は、タスクを識別する ZooKeeper クラスタ内でユニークな名前である。
スタンドアロン構成では、空文字列 (``""``) を指定する。

.. describe:: bool clear_row(0: string name, 1: string id)

   - 引数:

     - ``name`` : タスクを識別する ZooKeeper クラスタ内でユニークな名前
     - ``id`` : 削除する点 ID

   - 戻り値:

     - 点の削除に成功した場合 True 

   ID ``id`` で指定される点データを削除する。


.. describe:: tuple<string, float> add(0: string name, 1: datum row)

   - 引数

     - ``name`` : タスクを識別する ZooKeeper クラスタ内でユニークな名前
     - ``row`` : datum

   - 戻り値:

     - 点 ID と異常値のタプル

   点データ ``row`` を追加する。


.. describe:: float update(0: string name, 1: string id, 2: datum row)

   - 引数

     - ``name`` : タスクを識別する ZooKeeper クラスタ内でユニークな名前
     - ``id`` : 更新する点 ID
     - ``row`` : 点の新しいデータ

   - 戻り値:

     - 異常値

   点 ``id`` をデータ ``row`` で更新する。


.. describe:: bool clear(0: string name)

   - 引数

     - ``name`` : タスクを識別する ZooKeeper クラスタ内でユニークな名前

   - 戻り値:

     - モデルの削除に成功した場合 True

   モデルを完全に消去する。


.. describe:: float calc_score(0: string name, 1: datum row)

   - 引数

     - ``name`` : タスクを識別する ZooKeeper クラスタ内でユニークな名前
     - ``row`` : datum

   - 戻り値:

     - 与えられたデータに対する異常度

   点を追加せずに、与えられた点データ ``row`` の異常度を計算する。


.. describe:: list<string> get_all_rows(0: string name)

   - 引数

     - ``name`` : タスクを識別する ZooKeeper クラスタ内でユニークな名前

   - 戻り値:

     - すべての点の ID リスト

   すべての点の ID リストを返す。

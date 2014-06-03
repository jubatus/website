Unlearner
----------

* このアルゴリズムは単品では使用されず、 :doc:`classifier`, :doc:`nearest_neighbor`, :doc:`anomaly` のconfig経由で指定され利用される。

Configuration
~~~~~~~~~~~~~

設定は単体の JSON で与えられる。
JSON の各フィールドは以下のとおりである。

.. describe:: unlearner

   忘却に使用するアルゴリズムを下記の2つから選択する。

   .. table::

      ================ ===================================
      設定値           手法
      ================ ===================================
      ``"randomn"``    ランダムに要素を削除する。
      ``"lru"``        Least Recently Usedに従い要素を削除する。
      ================ ===================================

.. describe:: unlearner_parameter

   アルゴリズムに渡すパラメータを指定する。
   これは両アルゴリズムで共通である。

   :max_size:
     保持するデータの件数を指定する。
     小さくするほどメモリ消費量が低下し、処理時間が高速になり、精度が劣化する。
     (Integer)

     * 値域: 0 < ``max_size`` < 2147483647

.. describe:: 例

   .. code-block:: javascript

      {
        "unlearner_method" : "lru",
        "unlearner_parameter" : 16777216
      }

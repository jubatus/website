Unlearner
----------

* このアルゴリズムは単品では使用されず、 :doc:`api_classifier`, :doc:`api_nearest_neighbor`, :doc:`api_anomaly` のconfig経由で指定され利用される。

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

   :sticky_pattern:
     忘却の対象外とする ID のパターンを指定する。
     パターンの指定方法は :doc:`fv_convert` の適用規則で使用される ``key`` と同様である。
     ``lru`` 利用時のみ指定できる。
     (String)

.. describe:: 例

   .. code-block:: javascript

      {
        "unlearner_method" : "lru",
        "unlearner_parameter" : 16777216
      }

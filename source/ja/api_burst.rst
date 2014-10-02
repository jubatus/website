Burst
-----

* 詳細な仕様は `IDL 定義 <https://github.com/jubatus/jubatus/blob/master/jubatus/server/server/burst.idl>`_ を参照してください。

Configuration
~~~~~~~~~~~~~

設定は単体の JSON で与えられる。
JSON の各フィールドは以下のとおりである。

.. describe:: method

   バースト検知に使用するアルゴリズムを指定する。
   以下のアルゴリズムを指定できる。

   .. table::

      ==================== ===================================
      設定値               手法
      ==================== ===================================
      ``"burst"``          Kleinberg のバースト検知を利用する。
      ==================== ===================================

.. describe:: parameter

   アルゴリズムに渡すパラメータを指定する。
   ``method`` に応じて渡すパラメータは異なる。

   burst
     :window_batch_size:
        ウィンドウに含まれるバッチの数。
        (Integer)

        * 値域: 0 < ``window_batch_size``

     :batch_interval:
        1つのバッチの(位置の)間隔。
        (Double)

        * 値域: 0 < ``batch_interval``

     :max_reuse_batch_num:
        バッチの最大の再利用数。
        値が大きいほど、計算量を削減することができる。
        (Integer)

        * 値域: 0 <= ``max_reuse_batch_num`` <= ``window_batch_size``

     :costcut_threshold:
        コストカットの閾値。
        値が小さいほど、計算量を削減することができる。
        負の値を指定すると、コストカットを行わない (DBL_MAX) となる。
        (Double)

        * 値域: 0 <= ``costcut_threshold``

     :result_window_rotate_size:

        現在のウィンドウを含めた、メモリ上に保持するバッチの総数。
        (Integer)

        * 値域: 0 < ``window_batch_size`` <= ``result_window_rotate_size``

Data Structures
~~~~~~~~~~~~~~~

.. mpidl:message:: st_keyword

   バースト検知の対象となるキーワードとそのパラメタを表す。

   .. mpidl:member:: 0: string keyword

      バースト検知対象のキーワードを表す。

   .. mpidl:member:: 1: double scaling_param

      このキーワードに適用されるスケーリングパラメタを表す。

      * 値域: 0 < ``scaling_param``

   .. mpidl:member:: 2: double gamma

      このキーワードに適用されるγ値を表す。
      大きい値に設定するほど、バースト検知の感度が低くなる。

      * 値域: 0 < ``gamma``

   .. code-block:: c++

      message st_keyword {
        0: string keyword
        1: double scaling_param
        2: double gamma
      }

.. mpidl:message:: st_batch

   一つのバッチ区間内におけるバースト検知結果を表す。

   .. mpidl:member:: 0: int d

      バッチに登録された全文書の数を表す。

      * 値域: 0 < ``d``

   .. mpidl:member:: 1: int r

      バッチに登録された文書のうち、キーワードを含む文書の数を表す。

      * 値域: 0 < ``d`` <= ``r``

   .. mpidl:member:: 2: double burst_weight

      バースト具合の大きさ (バーストレベル、バッチ weight) を表す。
      バーストレベルは相対的な値であり、複数のキーワード間で相互に値を比較することはできない。

      * 値域: 0 <= ``burst_weight``

   .. code-block:: c++

      message st_batch {
        0: int d
        1: int r
        2: double burst_weight
      }

.. mpidl:message:: st_window

   バースト検知の結果を表す。

   .. mpidl:member:: 0: double start_pos

      このウィンドウの開始位置を表す。

   .. mpidl:member:: 1: list<st_batch> batches

      このウィンドウを構成するバッチの集合を表す。

   .. code-block:: c++

      message st_window {
        0: double start_pos
        1: list<st_batch> batches
      }

.. mpidl:message:: st_document

   バースト検知の対象とする文書データを表す。

   .. mpidl:member:: 0: double pos

      文書データの時系列的な位置 (一般的には時間) を表す。

   .. mpidl:member:: 1: string text

      文書データの内容を表す。
      文書データの内容が登録済みのキーワードを含むか否かは部分一致により判定される。

   .. code-block:: c++

      message st_document {
        0: double pos
        1: string text
      }

Methods
~~~~~~~

.. mpidl:service:: burst

   .. mpidl:method:: int add_documents(0: list<st_document> data)

      :param data:   登録する文書のリスト
      :return:       登録に成功した件数 (すべて成功すれば ``data`` の長さに等しい)

      バースト検知の対象とする文書を登録する。
      この API は ``st_document`` をリスト形式でまとめて同時に受け付けることができる (バルク更新)。

      学習を行う前に、予めキーワードを ``add_keyword`` メソッドで登録しておく必要がある。

      現在のウィンドウから外れた位置(``pos``)を持つ文書は登録することができない。

   .. mpidl:method:: st_window get_result(0: string keyword)

      :param keyword:  結果を取得するキーワード
      :return:         バースト検知結果

      登録済みのキーワード ``keyword`` に対する、現在のウィンドウにおけるバースト検知結果を取得する。

   .. mpidl:method:: st_window get_result_at(0: string keyword, 1: double pos)

      :param keyword:  結果を取得するキーワード
      :param pos:      位置
      :return:         バースト検知結果

      登録済みのキーワード ``keyword`` に対する、指定された位置 ``pos`` におけるバースト検知結果を取得する。

   .. mpidl:method:: map<string, st_window > get_all_bursted_results()

      :return:         キーワードとバースト検知結果の組

      すべてのキーワードに対する、現在のウィンドウにおけるバースト検知結果を取得する。

   .. mpidl:method:: map<string, st_window > get_all_bursted_results_at(0: double pos)

      :param pos:      位置
      :return:         キーワードとバースト検知結果の組

      すべてのキーワードに対する、指定された位置 ``pos`` におけるバースト検知結果を取得する。

   .. mpidl:method:: list<st_keyword> get_all_keywords()

      :return:         キーワードとバースト検知結果の組

      バースト検知対象として登録されているすべてのキーワードを取得する。

   .. mpidl:method:: bool add_keyword(0: st_keyword keyword)

      :param keyword:  追加するキーワードとパラメタ
      :return:         キーワードの追加に成功した場合 True

      キーワード ``keyword`` をバースト検知対象として登録する。

   .. mpidl:method:: bool remove_keyword(0: string keyword)

      :param keyword:  削削するキーワード
      :return:         キーワードの削除に成功した場合 True

      キーワード ``keyword`` をバースト検知対象から削除する。

   .. mpidl:method:: bool remove_all_keywords()

      :return:         キーワードの削除に成功した場合 True

      すべてのキーワードをバースト検知対象から削除する。

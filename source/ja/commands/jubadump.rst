jubadump
========

Synopsis
--------------------------------------------------

.. code-block:: shell

  jubadump -i <file> [options ...]

Description
--------------------------------------------------

``jubadump`` は ``save`` RPC によって保存された Jubatus のモデルファイルの内容を JSON 形式に変換するツールである。

現在、 ``classifier`` および ``recomender`` の ``inverted_index`` のみがサポートされている。

Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``[]`` はデフォルト値を意味する。

.. program:: jubadump

.. option:: -i <file>, --input <file>

   変換するモデルファイルへのパスを指定する。

.. option:: -t <format>, --type <format>

   入力ファイルのフォーマット。 [classifier]

   ``<format>`` には ``classifier`` または ``inverted_index`` のいずれかを指定する。

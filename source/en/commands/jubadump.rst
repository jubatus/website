jubadump
========

Synopsis
--------------------------------------------------

.. code-block:: shell

  jubadump -i <file> [options ...]

Description
--------------------------------------------------

``jubadump`` is a tools to convert Jubatus model files saved using ``save`` RPC to JSON.

Currently, only ``classifier`` and ``inverted_index`` of ``recommender`` are supported.

Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``[]`` indicates the default value.

.. program:: jubadump

.. option:: -i <file>, --input <file>

   Path of the model file to convert.

.. option:: -t <format>, --type <format>

   Format of the input file [classifier]

   ``<format>`` must be one of ``classifier`` or ``inverted_index``.

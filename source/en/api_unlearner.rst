Unlearner
----------

* This algorithm is used only via configurations of :doc:`classifier` or :doc:`nearest_neighbor` or :doc:`anomaly`.

Configuration
~~~~~~~~~~~~~

Configuration is given as a JSON file.
We show each field below:

.. describe:: unlearner

   Specify unlearning strategy from below two.

   .. table::

      ================ ===================================
      設定値           手法
      ================ ===================================
      ``"randomn"``    Delete data randomly
      ``"lru"``        Delete data upon Least-Recently-Used strategy
      ================ ===================================

.. describe:: unlearner_parameter

   Specify parameters for the algorithm.
   Its format is common for each unlearner strategy.

   :max_size:
     Specify the upper-limit of data quantity.
     The smaller it is, the less memory usage, the more fast, the less accurately.

.. describe:: example

   .. code-block:: javascript

      {
        "unlearner_method" : "lru",
        "unlearner_parameter" : 16777216
      }

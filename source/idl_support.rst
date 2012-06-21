IDL Support Status (2011/06/06)
-------------------------------------------

Currently, Jubatus supports four machine learning services (Classifier, Regression, Recommender, Stat). The followings are support status of msgpack-idl.

+------------+------------+-------------+--------------+--------------+ 
|            | Classifier | Regression  | Recommender  | Stat         |
+------------+------------+-------------+--------------+--------------+ 
| C++        | ok          | ok           |  ok           | ok            |
+------------+------------+-------------+--------------+--------------+ 
| Java       | △          |  △          | △            | △            |
+------------+------------+-------------+--------------+--------------+ 
| Python     | ok          |  ok          |  ok           | ok            |
+------------+------------+-------------+--------------+--------------+ 
| Ruby       | ok          |  ok          |  ok           | ok            |
+------------+------------+-------------+--------------+--------------+ 

Symbol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ok：We can use generated clients.

- △：We ned to make some minor changes t ogenerated client.

  - We appreciate you if you gave us patchs to msgpack-idl.


Specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We tested these clients in the following condition

- Jubatus : Jubatus 0.2.3

- Server : Built-in servers in repository

- Client : Generated client from IDL

- IDL : Built-in IDL in repository


All Clients are available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This support status suggests that we can support clients of all existing service in four languages mentioned above. And actually, we do. Clients of all types are available from `this download page <https://github.com/jubatus/jubatus/downloads>`_



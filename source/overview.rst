Overview
==========

Jubatus is a distributed online machine learning framework for processing very large-scale data.

Jubatus supports many ways of data analysis tools in online and scalable manner; classification, regression, statistics, and recommendation.

Jubatus uses unique computational archtecture, Update Analyaze, and Mix, which enables efficient model training, sharing, and applying, respectively in a similar way with the Map and Reduce operations.

Scalable
--------

Jubatus supports scalable machine learning processing. It can handle 100000 or more data per second using commodity hardware clusters. It is designed for clusters of commodity, shared-nothing hardware.

Real-Time
--------

Jubatus updates a model instantaneously just after recieving a data, and it analyze the data instantaneously

Deep-Analysis
-------------

Jubatus supports many ways of deep analysis; classification, regression, statistics, and recommendation.


Difference from Hadoop and Mahout
---------------------------------

There many similar points between Hadoop/Mahout and Jubatus. These are scalable  and run on commodity hardware.
However, while Hadoop/Mahout processes data in batch manner and achieve high throughput, Jubatus processes data in online manner, and achieve high throughput and low latency.
To achieve these features togather, 
Jubatus uses an unique loosely model synchronization for scale out and fast model sharing in distributed environments.
Jubatus processes all data in memory, and focus on operations for data analysis. 

Administrator's Guide
=====================

This section is a guide for system administrators.


Recommended process configuration
---------------------------------

For reliable Jubatus service, you should run Jubatus on distributed environment.
And then, for high performance, you should be serious about the process configuration of Jubatus and processes that Jubatus depends on.

This is the process configuration that we recommend.

.. figure:: ../_static/process_configuration.png
   :width: 90 %
   :alt: process configuration

Jubakeeper
~~~~~~~~~~

We recommend the configration that Jubakeeper and Client-Application will be a one-to-one. Because, ease of operation and implementation of the application.

For case that Client-Application can not connect to Jubakeeper (ex. Jubakeeper is downed), it is necessary to consider the reliability depending on the services provided. For example, like the following:

#. Monitor the process. If Client-Application can not connect to Jubakeeper, blocks the access to Client-Application.
#. Switch to another Jubakeeper.

Jubaserver
~~~~~~~~~~

If you set same name using ``--name`` options, processes collaborate with one another. As long as one of processes is running, Jubatus is available.

In the figure above, processes is distributed on ``N + 1`` machines. Even when a failure occurs in ``N`` of machines, all of instances available.

Jubatus processes all data in memory. In order to prevent the lack of resourses (specially memory), you should pay to attention to the placement of the process.

Zookeeper
~~~~~~~~~

When running Jubatus on distributed environment, It is a fatal condition that Zookeeper is not available. For reliable ZooKeeper service, you should note the following:

#. Deploy ZooKeeper in a cluster as known an ensemble using an odd number of machines.
#. For minimization that sort of degradation, deploy Zookeeper on a dedicated machine.

For details, See `the documentation of Zookeeper <http://zookeeper.apache.org/doc/current/>`_ .

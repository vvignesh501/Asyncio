Home assignment
===============

The given project contains some code smells, bugs, and rush design decisions. Please improve the code
design and get rid of the worst code smells.

We don't want this assignment to take more then one hour of your time, but you're welcome to spend
as much time as you want on it. In case if you see that you've already spent a lot of time on the
assignment, but there is still some issues left, you can write a list of things that are left to be
improved, but please be specific.

Project description
-------------------

Provided solution is a web service that is similar to on-line trading platform.
It allows users to view products, create an order, view order details,
history of the orders, and manage orders.

The solution is built on the top of stable service developed be the company years ago and uses `lib.py`
to communicate with it. The solution also depends on a couple of other services.


Details
--------

The service (represented by `service.py`) just became public and already has some users. There are
some competitors and we'd like to beat them by non functional requirement and features delivery speed
of our solution. The API lib (represented by `lib.py`) is a stable product with next stable release
scheduled in 5 years time.

Please re-factor the `service.py` and `lib.py`.

How to install
--------------

.. code-block:: bash

    pip install aiohttp


How to run
-----------

.. code-block:: bash

    python service.py

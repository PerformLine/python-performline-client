Using the Client and Retrieving Compliance Data
===================================================================================================

Overview
-------------------------------------------------

Using the PerformMatch Compliance API is fairly straightforward.  The API is accessed by way of a
:class:`~performline.client.Client()` instance created with your API token (provided by PerformLine
Support).  The client instance exposes methods that allow you to access the various data associated
with your account.  To explore these methods, see the second below detailing what can be accessed for
each product that we offer.


Products & Data
-------------------------------------------------

The methods in the following classes are the primary means of accessing product-specific data and,
in general, using the API.  These classes are _mixins_, so each of the methods are available on an
instance of :class:`~performline.client.Client()`.

Mix-in Classes
^^^^^^^^^^^^^^
.. toctree::
   :glob:
   :maxdepth: 1

   products/common
   products/web
   products/callcenter
   products/chatscout

Client Class Reference
-------------------------------------------------

.. automodule:: performline.client
   :members:

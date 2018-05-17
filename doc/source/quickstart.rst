Quick Start
===================================================================================================

This page will offer a quick overview for how to get started with using this library, from
installation to basic usage.


Installation
-------------------------------------------------

This library is made available for installation via the PyPi public Python package
repository (https://pypi.python.org/pypi/performline/).  To install it on your machine, run:

.. code-block:: bash
   :linenos:

   pip install performline

This will retrieve the latest version of the Python module and install it.  This will also install
a useful command line utility called ``performline``.  You can read more about using this command by
running ``performline --help``.


Basic Usage: Printing all Brands and Campaigns
-------------------------------------------------

.. code-block:: python
   :linenos:

   from performline.client import Client
   import json

   client = Client("YOUR_API_KEY")

   # list all brands
   for brand in client.brands():
      print("Brand: {} (id: {})".format(brand.name, brand.id))

      # list all campaigns in the current brand
      for campaign in brand.campaigns():
         print("    Campaign: {}".format(campaign.name))

         # output the full content of each item in the current campaign
         for item in campaign.items():
            print(json.dumps(item._data, indent=4))
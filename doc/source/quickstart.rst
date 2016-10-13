Quick Start
===================================================================================================

This page will offer a quick overview for how to get started with using this library, from
installation to basic usage.


Installation
-------------------------------------------------

This library is made available for installation via the PyPi public Python package
repository (https://pypi.python.org/pypi/performline/).  To install it on your machine, run:

.. code-block:: bash
    pip install performline

This will retrieve the latest version of the Python module and install it.  This will also install
a useful command line utility called `performline`.  You can read more about using this command by
running `performline --help`.


Basic Usage: Printing all Brands and Campaigns
-------------------------------------------------

.. code-block:: bash
    from performline.client import Client

    c = Client("YOUR-API-KEY")

    # list the name and id of all brands
    for brand in c.brands():
        print("Brand: %s (id = %d)" % (brand.name, brand.id))

    # list details about all campaigns
    for item in c.campaigns():
        # retrieve complete details on this campaign
        campaign = c.campaigns(item.id)

        # load the brand associated with this campaign
        brand = campaign.brand

        print("Campaign: %s" % campaign.name)
        print("  For Brand: %s (id = %d)" % (brand.name, brand.id))
        print("  Pages:     %d" % campaign.num_pages)
        print("  Score:     %d" % campaign.num_pages)

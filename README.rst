Bynder Python SDK
=================

The main goal of this SDK is to speed up the integration of Bynder
customers who use Python. Making it easier to connect to the Bynder API
(http://docs.bynder.apiary.io) and execute requests on it.

Requirements and dependencies
-----------------------------

The Python SDK requires the following in order to fully work:

-  ``Python >= 3.5``, older versions of Python won't work.

Pip should handle all the dependencies automatically.

Installation
------------

This SDK depends on a few libraries in order to work, installing it with
pip should take care of everything automatically.

Before you install the SDK we recommend you to setup a virtual
environment:

.. code:: bash

    virtualenv -p python3 venv  # create virtual environment
    source venv/bin/activate    # activate virtual environment

After you have successfully setup a virtual environment you can install
the SDK with `pip <https://pip.pypa.io/en/stable/installing/>`__. Run
the following command while your virtual environment is active.

.. code:: bash

    pip install bynder-sdk

To use the SDK, you have to import it at the top of your file:

.. code:: python

    from bynder_sdk import BynderClient 

How to use it
-------------

This is a simple example on how to retrieve data from the Bynder asset
bank. For a more detailed example of implementation refer to the `sample
code <https://github.com/Bynder/bynder-python-sdk/blob/master/example/app.py>`__.

Before executing any request to the Bynder API we need to instantiate
the **BynderClient** class, the following example shows how to do this:

.. code:: python

        bynder_client = BynderClient(
            base_url=config.get('BYNDER_TOKENS', 'base_url'),
            consumer_key=config.get('BYNDER_TOKENS', 'consumer_key'),
            consumer_secret=config.get('BYNDER_TOKENS', 'consumer_secret'),
            token=config.get('BYNDER_TOKENS', 'token'),
            token_secret=config.get('BYNDER_TOKENS', 'token_secret')
        )

We encourage you to store the tokens in a `configuration
file <https://docs.python.org/3/library/configparser.html>`__ or as
envrioment variables. This will help you to keep your tokens safe.

After getting the **BynderClient** configured successfully we need to
get an instance of the **AssetBankClient** in order to do any of the API
calls relative to the Bynder Asset Bank module:

.. code:: python

         asset_bank_client = bynder_client.asset_bank_client
         collection_client = bynder_client.collection_client # Works the same

And with this, we can start our request to the API, listed in the
**Methods Available** section following. Short example of getting all
the **Media Items**:

.. code:: python

        media_list = asset_bank_client.media_list()

This call will return a list with all the Media Items available in the
Bynder environment. Note that some of the calls accept a query array in
order to filter the results via the API call params (see `Bynder API
Docs <http://docs.bynder.apiary.io/>`__) for more details. For instance,
if we only wanted to retrieve **2 images** here is what the call would
look like:

.. code:: python

        media_list = asset_service.media_list({
            'limit': 2,
            'type': 'image'
        })

Methods Available
-----------------

These are the methods currently availble on the **Bynder Python SDK**,
refer to the `Bynder API Docs <http://docs.bynder.apiary.io/>`__ for
more specific details on the calls.

BynderClient:
^^^^^^^^^^^^^

Get an instance of the Asset Bank Client or the Collection Client if
already with access tokens set up. Also allows to generate and
authenticate request tokens, which are necessary for the rest of the
Asset Bank and Collection calls.

.. code:: python

        asset_bank_client
        collection_client
        login()
        request_token()
        authorise_url()
        access_token()
        logout()
        derivatives()

asset\_bank\_client:
^^^^^^^^^^^^^^^^^^^^

All the Asset Bank related calls, provides information and access to
Media management.

.. code:: python

        brands()
        media_list(query)
        media_info(media_id, query)
        meta_properties()
        tags()
        media_download_url()
        set_media_properties(media_id, query)
        delete_media(media_id)
        create_usage(itegration_id, asset_id, query)
        usage(query)
        delete_usage(integration_id, asset_id, query)
        upload_file(file_path, brand_id, media_id, query)

With the ``upload_file`` method you can do two things. You can upload a
new asset, or you can upload a new version of an exising asset. You can
control this by sending a media\_id or not.

collection\_client:
^^^^^^^^^^^^^^^^^^^

All the collection related calls.

.. code:: python

        collections(query)
        collections_info(collection_id)
        create_collection(name, query)
        delete_collection(collection_id)
        collection_media_ids(collection_id)
        add_media_to_collection(collection_id, media_ids)
        remove_media_from_collection(collection_id, meedia_ids)
        share_collection(collection_id, collection_option, recipients, query)

pim\_client:
^^^^^^^^^^^^

All the PIM related calls.

.. code:: python

    metaproperties()
    metaproperty_info(metaproperty_id)
    metaproperty_options(metaproperty_id)
    edit_metaproperty_option(metaproperty_option_id, children)

workflow\_client:
^^^^^^^^^^^^^^^^^

All the workflow related calls.

.. code:: python
        users()
        groups()
        group_info(group_id)
        metaproperties()
        metaproperty_info(metaproperty_id)
        campaigns(query)
        campaign_info(campaign_id)
        create_campaign(name, key, description, responsibleID, query)
        edit_campaign(campaign_id, name, key, description, responsibleID, query)
        delete_campaign(campaign_id)
        job_preset_info(job_preset_info)
        jobs(campaign_id)
        create_job(name, campaignID, accountableID, presetID, query)
        edit_job(job_id, name, campaignID, accauntableID, presetID, query)
        job_info(job_id)
        delete_job(job_id)

Tests
-----

You can run the tests by using the command below. This will install the
packages required and execute the tests for all the clients.

.. code:: bash

    make test

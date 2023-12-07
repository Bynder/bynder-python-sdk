Bynder Python SDK
=================

![Tests](https://github.com/Bynder/bynder-python-sdk/workflows/Tests/badge.svg)
![Publish](https://github.com/Bynder/bynder-python-sdk/workflows/Publish/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/Bynder/bynder-python-sdk/badge.svg?branch=master)](https://coveralls.io/github/Bynder/bynder-python-sdk?branch=master)
![PyPI](https://img.shields.io/pypi/v/bynder-sdk)
![PyPI - Downloads](https://img.shields.io/pypi/dm/bynder-sdk?color=orange)

The main goal of this SDK is to speed up the integration of Bynder
customers who use Python. Making it easier to connect to the Bynder API
(<https://bynder.docs.apiary.io>) and execute requests on it.

_**Note:** As of version 1.0.0 this SDK now uses OAuth 2.0. For the last
version using OAuth 1.0a please refer to
[version 0.0.6](https://github.com/Bynder/bynder-python-sdk/tree/0.0.6)_.

Requirements and dependencies
-----------------------------

The Python SDK requires the following in order to fully work:

-   `Python >= 3.5`, older versions of Python won't work.

Pip should handle all the dependencies automatically.

Installation
------------

This SDK depends on a few libraries in order to work, installing it with
pip should take care of everything automatically.

Before you install the SDK we recommend you to setup a virtual
environment:

```bash
virtualenv -p python3 venv  # create virtual environment
source venv/bin/activate    # activate virtual environment
```

After you have successfully setup a virtual environment you can install
the SDK with [pip](https://pip.pypa.io/en/stable/installing/). Run the
following command while your virtual environment is active.

```bash
pip install bynder-sdk
```

Getting started
---------------

This is a simple example on how to retrieve data from the Bynder asset
bank. For a more detailed example of implementation refer to the [sample
code](https://github.com/Bynder/bynder-python-sdk/blob/master/example/app.py).

First import the BynderClient:

```python
from bynder_sdk import BynderClient
```

When using OAuth2, create an instance of the client and use the flow
to receive a token:

```python
bynder_client = BynderClient(
    domain='portal.getbynder.com',
    redirect_uri='https://...',
    client_id='',
    client_secret='',
    token_saver=token_saver
)

print(bynder_client.get_authorization_url())
code = input('Code: ')
bynder_client.fetch_token(code)
```

When using a permanent token, the client instance can be created like this:

```python
bynder_client = BynderClient(
  domain='portal.getbynder.com',
  permanent_token=''
)
```

Finally call one of the API's endpoints through one of the clients:

```python
asset_bank_client = bynder_client.asset_bank_client
media_list = asset_bank_client.media_list({
    'limit': 2,
    'type': 'image'
})
```

A full list of the currently available clients and methods in the SDK
can be found below

Methods Available
-----------------

These are the methods currently availble on the **Bynder Python SDK**,
refer to the [Bynder API Docs](http://docs.bynder.apiary.io/) for more
specific details on the calls.

### BynderClient:

Get an instance of the Asset Bank Client or the Collection Client if
already with access tokens set up. Also allows to generate and
authenticate request tokens, which are necessary for the rest of the
Asset Bank and Collection calls.

```python
asset_bank_client
collection_client
pim_client
workflow_client
get_authorization_url()
fetch_token()
derivatives()
```

### asset\_bank\_client:

All the Asset Bank related calls, provides information and access to
Media management.

```python
brands()
tags()
meta_properties()
media_list(query)
media_info(media_id, query)
media_download_url()
set_media_properties(media_id, query)
delete_media(media_id)
create_usage(itegration_id, asset_id, query)
usage(query)
delete_usage(integration_id, asset_id, query)
upload_file(file_path, brand_id, media_id, query)
```

With the `upload_file` method you can do two things. You can upload a
new asset, or you can upload a new version of an exising asset. You can
control this by sending a media\_id or not.

### collection\_client:

All the collection related calls.

```python
collections(query)
collection_info(collection_id)
create_collection(name, query)
delete_collection(collection_id)
collection_media_ids(collection_id)
add_media_to_collection(collection_id, media_ids)
remove_media_from_collection(collection_id, meedia_ids)
share_collection(collection_id, collection_option, recipients, query)
```

### pim\_client:

All the PIM related calls.

```python
metaproperties()
metaproperty_info(metaproperty_id)
metaproperty_options(metaproperty_id)
edit_metaproperty_option(metaproperty_option_id, children)
```

### workflow\_client:

All the workflow related calls.

```python
users()
campaigns(query)
campaign_info(campaign_id)
create_campaign(name, key, description, responsibleID, query)
delete_campaign(campaign_id)
edit_campaign(campaign_id, name, key, description, responsibleID, query)
metaproperties()
metaproperty_info(metaproperty_id)
groups()
group_info(group_id)
job_preset_info(job_preset_info)
jobs(campaign_id)
create_job(name, campaignID, accountableID, presetID, query)
job_info(job_id)
edit_job(job_id, name, campaignID, accauntableID, presetID, query)
delete_job(job_id)}
```

Tests
-----

You can run the tests by using the command below. This will install the
packages required and execute the tests for all the clients.

```bash
make test
```

Docker Setup Guide
-----------------

The Docker setup allows you to run your Python scripts inside a Docker container, with dependencies installed and files synchronized. This guide aims to facilitate the development and testing of the SDK.

### Requirements and dependencies

Ensure the following are installed on your machine:

-   [Docker](https://www.docker.com/get-started/)
-   [docker-compose](https://docs.docker.com/compose/)

### Initial Setup

Create a `secret.json` file by following the example provided in the project. Fill in the necessary settings based on your requirements. If you have a permanent token, only the domain and permanent_token fields need to be specified:
 ```
 {
    "domain": "example.bynder.com", # Without the http:// or https://
    "permanent_token": "7d09..........."
}
 ```

With `docker` and `docker-compose` installed, and your `secret.json` file ready, run the following command to initiate the container:
```bash
make run-docker
```
This command initializes a container with the bynder-python-sdk installed and ready for use.

### Executing SDK Samples

You can utilize the `Makefile` commands on your console to run SDK sample scripts. The syntax is as follows:
```bash
make executeSdkSample sample-file-name=file.py
```
All sample files are located in the `./samples` directory.

> :warning: Caution: The sample scripts are provided as examples. It is crucial to review, add and/or modify the commands before execution. The container updates automatically with changes, ensuring a seamless development experience. Always exercise caution when executing scripts.

## Stopping the Docker Container

When you're done with your development or testing, you can stop the Docker container using the following command:

```bash
make stop-docker
```

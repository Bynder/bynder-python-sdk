# Examples

The SDK contains multiple examples to show how the SDK can be used.

## Executing examples

In order to execute the examples, you will have to first configure the
OAuth2 credentials. This can be done in two ways:
1. By saving them to [config.ini](config.ini)
2. By setting the configuration as environment variables
(e.g. `export BYNDER_DOMAIN=portal.getbynder.com`)

A combination of the two can also be used, in which case environment
variables override values in [config.ini](config.ini).

With the configuration done examples can simply be called by executing
`python example.py` or `python -m example` after installing the SDK
(i.e. by running `pip install .` in the root folder).

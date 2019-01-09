class PIMClient:
    """ Client used for all the operations that can be done to PIM.
    """
    def __init__(self, bynder_request_handler):
        self.bynder_request_handler = bynder_request_handler

    def metaproperties(self):
        """ Gets list of metaproperties.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/pim/metaproperties/'
        )

    def metaproperty_info(self, metaproperty_id):
        """ Get metaproperty info about a specific metaproperty.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/pim/metaproperties/{}/'.format(metaproperty_id)
        )

    def metaproperty_options(self, metaproperty_id, query: dict = None):
        """ Get list of metaproperty options.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/pim/metaproperties/{}/options/'.format(
                metaproperty_id),
            params=query or {}
        )

    def edit_metaproperty_option(self, metaproperty_option_id, children):
        """ Edits an existing metaproperty option.
        """
        if isinstance(children, str):
            children = [children]
        return self.bynder_request_handler.put(
            endpoint='/api/pim/metapropertyoptions/{}/'.format(
                metaproperty_option_id),
            json={'children': children}
        )

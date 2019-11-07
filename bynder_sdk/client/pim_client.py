class PIMClient:
    """ Client used for all the operations that can be done to PIM.
    """
    def __init__(self, session):
        self.session = session

    def metaproperties(self):
        """ Gets list of metaproperties.
        """
        return self.session.get(
            endpoint='/pim/metaproperties/'
        )

    def metaproperty_info(self, metaproperty_id):
        """ Get metaproperty info about a specific metaproperty.
        """
        return self.session.get(
            endpoint='/pim/metaproperties/{}/'.format(metaproperty_id)
        )

    def metaproperty_options(self, metaproperty_id, query: dict = None):
        """ Get list of metaproperty options.
        """
        return self.session.get(
            endpoint='/pim/metaproperties/{}/options/'.format(
                metaproperty_id),
            params=query or {}
        )

    def edit_metaproperty_option(self, metaproperty_option_id, children):
        """ Edits an existing metaproperty option.
        """
        if isinstance(children, str):
            children = [children]
        return self.session.put(
            endpoint='/pim/metapropertyoptions/{}/'.format(
                metaproperty_option_id),
            json={'children': children}
        )

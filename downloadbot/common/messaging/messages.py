# -*- coding: utf-8 -*-


class Message:

    def __init__(self, id, body, delivery_receipt):

        """
        Parameters
        ----------
        id : str
            Unique identifier.
        body : str
            Content.
        delivery_receipt : str
            Unique identifier associated with the transaction of
            receiving this message.
        """

        self.id = id
        self.body = body
        self.delivery_receipt = delivery_receipt

    def __repr__(self):
        repr_ = '{}(id="{}", body="{}", delivery_receipt="{}")'
        return repr_.format(self.__class__.__name__,
                            self.id,
                            self.body,
                            self.delivery_receipt)

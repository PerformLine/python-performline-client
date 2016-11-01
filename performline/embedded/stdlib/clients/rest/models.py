from __future__ import absolute_import
import json
from ...utils.dicts import deep_get, camelize, camelize_dict, underscore_dict
from ...utils.dicts import compact as utils_compact
from .exceptions import UnsupportedOperation


class RestModel(object):
    """
    Represents individual objects that can be read, created, and/or update via a given client.

    Args:
        rest_root (str, abstract): The path that will be called when operating on this model
            object.  All interactions with objects of this type will have this path prepended to
            them when making HTTP calls.  For operations on specific instances, this value will be
            combined with ``primary_key`` to form the final path.  For example:

            If ``rest_root = '/example/'`` and ``primary_key = 'id'``, the pattern for retrieving a
            single object will be "/example/{id}/".  This path will will then have the `format()`
            method called on it whenever it is used with the current value of the ``data`` property
            passed in as `**kwargs`.  This allows data values to be interpolated into the path at
            call time.

            This value must be set (explictly during instantiation or implicitly in a subclass)
            before the class can be used.

        rest_read_method (str, optional): The HTTP method that will be used for retrieving the
            object this instance represents.

        rest_create_method (str, optional): The HTTP method that will be used for creating the
            object this instance represents.

        rest_update_method (str, optional): The HTTP method that will be used for updating the
            object this instance represents.
    """

    primary_key = 'id'
    rest_read_method = 'get'
    rest_create_method = 'post'
    rest_update_method = 'put'

    def __init__(self, client, data=None, metadata={}, rest_root=None, primary_key=None):
        """
        Provides a simplified interface for working with standard REST API responses.

        Args:
            client (:class:`~performline.clients.rest.StandardRestClient`): The REST client that
                was used to retrieve the data or one that will be used to persist it.

            data (dict): The dictionary that represents this model.

            rest_root (str, optional): If specified, this will set or override the base path this
                instance uses to retrieve or persist data.

            primary_key (str, optional): If specified, this field name will be used for all
                operations that occur on a specific instance of this object.
        """

        if rest_root is not None:
            self.rest_root = rest_root

        if primary_key is not None:
            self.primary_key = primary_key

        if not hasattr(self, 'rest_root') or self.rest_root is None:
            raise AttributeError("Cannot create RestModel instance without a "
                                 "valid 'rest_root' attribute")

        if not hasattr(self, 'primary_key') or self.primary_key is None:
            raise AttributeError("Cannot create RestModel instance without a "
                                 "valid 'primary_key' attribute")

        self.__metadata = metadata
        self._client = client

        if data is not None:
            self.set_data(data)

    @classmethod
    def get(cls, client, pk):
        return cls(client, {
            cls.primary_key: pk,
        }).retrieve()

    @classmethod
    def all(cls, client, **kwargs):
        items = []

        for response in client.get_until(cls.rest_root, **kwargs):
            # for each result
            for item in response.results():
                # format the list result item the same way formatted_path would
                item = underscore_dict(item)

                # get the value of the primary key field
                pk = item.get(cls.primary_key)

                if pk is not None:
                    instance = cls(client, {
                        cls.primary_key: pk,
                    })

                    instance.retrieve()
                    items.append(instance)

        return items

    @property
    def pk(self):
        return self._data.get(self.primary_key)

    @property
    def _data(self):
        """
        Retrieves the underlying data that this model represents.

        Returns:
            dict
        """
        if self.__data is None:
            return {}
        return self.__data

    @property
    def _metadata(self):
        return self.__metadata

    @property
    def instance_path(self):
        return self.rest_root.rstrip('/') + '/{' + self.primary_key.strip('/') + '}/'

    def formatted_path(self, additional_args={}):
        """
        Returns the ``instance_path`` with data (and, if specified, additional/override arguments)
        interpolated in.  This method uses the standard Python ``format()`` function.

        Returns:
            str
        """

        kwa = {}

        for k, v in underscore_dict(self._data).items():
            kwa[k] = getattr(self, k)

        kwa.update(additional_args)
        return self.instance_path.format(**kwa)

    def set_data(self, data):
        """
        Updates the model's underlying data, processing it with :func:`prepare_data_from_retrieval`
        first.
        """
        self.__data = self.prepare_data_from_retrieval(data)

    def set_metadata(self, metadata):
        """
        Updates the model's metadata, processing it with :func:`prepare_metadata_from_retrieval`.
        first.
        """
        self.__metadata = self.prepare_metadata_from_retrieval(metadata)

    def prepare_data_from_retrieval(self, data):
        """
        A method used to prepare data as retrieved from the client in response to a retrieve (GET)
        request.  This default implementation processes the data through
        :func:`~performline.utils.dicts.camelize_dict`, but can be overridden in a subclass to
        perform custom post-processing.

        Returns:
            dict of post-processed data.
        """
        return camelize_dict(data, True)

    def prepare_metadata_from_retrieval(self, metadata):
        """
        A method used to prepare metadata as retrieved from the client in response to a
        retrieve (GET) request.  This default implementation passes the metadata to
        :func:`prepare_data_from_retrieval`, but can be overridden in a subclass to perform custom
        post-processing.

        Returns:
            dict of post-processed metadata.
        """

        return self.prepare_data_from_retrieval(metadata)

    def prepare_data_for_update(self, data):
        """
        A method used to prepare the model's data for submission to the service (POST/PUT). This
        default implementation is a no-op and returns the given ``data`` as-is, but can be
        overridden in a subclass to perform custom pre-processing.

        Args:
            data (dict): The model's data about to be sent to the upstream service.

        Returns:
            dict of pre-processed data.
        """
        return data

    @property
    def client(self):
        """
        Retrieves the client object that is used for interacting with services.

        Returns:
            :class:`~performline.clients.rest.StandardRestClient`
        """
        return self._client

    def retrieve(self):
        """
        Refreshes this model's internal representation with the server.
        """

        if self.rest_read_method is None:
            raise UnsupportedOperation("Retrieval is not supported on {0}".format(self.__class__))

        response = self.client.request(self.rest_read_method, self.formatted_path())
        result = response.results(0)

        self.set_data(result)
        self.set_metadata(response.metadata)

        return self

    def save(self, refresh=True, compact=False):
        """
        Persists this model's current data to the server.

        Args:
            refresh (bool): Whether to automatically refresh the model with the data that was
                just persisted.

            compact (bool, lambda, optional): Whether the data should be compacted before being
                submitted to the server.  If this is True, _None_ values will be removed.  If this
                is a lambda matching the signature ``f(key,value) -> bool``, that will be the
                function that determines which keys are kept (return True) and which are rejected
                (return False).

        Raises:
            AttributeError if the given ``key_attr`` is not a valid attribute on this instance.
        """

        if self.rest_create_method is None and self.rest_update_method is None:
            raise UnsupportedOperation("Persistence is not supported on {0}"
                                       .format(self.__class__))

        data = self._data

        # compacts the data (either with the default method or with a user-specified one)
        if compact:
            if isinstance(compact, type(lambda: 0)):
                data = utils_compact(data, compact)
            else:
                data = utils_compact(data)

        data = self.prepare_data_for_update(data)

        # performs the request
        self.client.request(self.rest_update_method,
                            self.formatted_path(),
                            data)

        # optionally refresh (read back) the data we just saved
        if refresh:
            return self.retrieve()

        return True

    def __getattr__(self, name):
        """
        Retrieves the named attribute as if it were a property if it exists in this model's
        response payload.  Otherwise, the attribute behaves normally.  Attributes that start
        with an underscore (_) will be passed along to the normal attribute handler as usual.

        Returns:
            any
        """
        if not name.startswith('_'):
            candidate_key = camelize(name, True)
            value = deep_get(self._data, name, deep_get(self._data, candidate_key))

            if value is not None:
                return value

    def __setattr__(self, name, value):
        key = camelize(name, True)

        if isinstance(self._data, dict) and key in self._data:
            print('Setting %s' % key)
            self._data[key] = value

        object.__setattr__(self, name, value)

    def __iter__(self):
        for key, value in self._data.items():
            yield (key, value)

    def __dict__(self):
        return self._data

    def __repr__(self):
        return json.dumps(self._data, indent=4)
    __str__ = __repr__

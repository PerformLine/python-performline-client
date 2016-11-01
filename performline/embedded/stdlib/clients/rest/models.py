from __future__ import absolute_import
import json
from ...utils.dicts import deep_get, camelize, camelize_dict, underscore_dict
from ...utils.dicts import compact as utils_compact
from .exceptions import UnsupportedOperation


class RestModel(object):
    """
    Represents individual objects that can be read, created, and/or update via a given client.

    Args:
        rest_path (str, abstract): The path that will be called when operating on this model
            object.  The path will have the `format()` method called on it whenever it is used with
            the current value of the ``data`` property passed in as `**kwargs`.  This allows you
            to interpolate data values into the path at call time.

            This value must be set (explictly during instantiation or implicitly in a subclass)
            before the class can be used.

        rest_read_method (str, optional): The HTTP method that will be used for retrieving the
            object this instance represents.

        rest_create_method (str, optional): The HTTP method that will be used for creating the
            object this instance represents.

        rest_update_method (str, optional): The HTTP method that will be used for updating the
            object this instance represents.
    """

    rest_read_method = 'get'
    rest_create_method = 'post'
    rest_update_method = 'put'

    def __init__(self, client, data, metadata={}, rest_path=None):
        """
        Provides a simplified interface for working with standard REST API responses.

        Args:
            client (:class:`~performline.clients.rest.StandardRestClient`): The REST client that
                was used to retrieve the data or one that will be used to persist it.

            data (dict): The dictionary that represents this model.

            rest_path (str, optional): If specified, this will set or override the path this
                instance uses to retrieve or persist data.
        """

        if rest_path is not None:
            self.rest_path = rest_path

        if not hasattr(self, 'rest_path') or self.rest_path is None:
            raise AttributeError("Cannot create RestModel instance without a "
                                 "valid 'rest_path' attribute")

        self.__metadata = metadata
        self._client = client
        self.set_data(data)

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

    def formatted_path(self, additional_args={}):
        """
        Returns the ``rest_path`` with data (and, if specified, additional/override arguments)
        interpolated in.  This method uses the standard Python ``format()`` function.

        Returns:
            str
        """

        kwa = {}

        for k, v in underscore_dict(self._data).items():
            kwa[k] = getattr(self, k)

        kwa.update(additional_args)
        return self.rest_path.format(**kwa)

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

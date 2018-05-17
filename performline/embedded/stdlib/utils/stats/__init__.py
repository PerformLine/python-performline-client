"""
Application monitoring and timeseries data collection utilities
"""
from __future__ import absolute_import
import re
from copy import deepcopy
import datetime
import statsd
from ..dicts import compact

TAG_VALUE_REPLACE = re.compile('[^0-9a-zA-Z\-\.]')


class Stats(object):
    """
    A helper class for reporting statistics to a specific stats backend.

    Args:
        host (str): The hostname of the StatsD-compatible service to report to.

        port (int): The port of the StatsD-compatible service to report to.

        prefix (str, optional): A string prefix that will be prepended to all measurements
            that pass through this instance.

        tags (dict, optional): A dictionary of key-value pairs that will be included with all stats
            that are emitted for systems that support faceted stats aggregation (e.g. Telegraf,
            OpenTSDB, KairosDB).

        enabled (bool): Whether metrics submission is enabled by default.
    """

    def __init__(self, host='localhost', port=8125, prefix=None, tags=None, enabled=True):
        self.host = host
        self.port = port
        self.prefix = prefix
        self.tags = tags
        self._statsd = statsd.StatsClient(self.host, self.port)
        self.enabled = enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_metric_name(self, metric, additional_tags=None):
        """
        Returns the metric name in a manner suitable for submission to the stats service.

        Args:
            metric (str): The name of the metric to format.

            additional_tags (dict, optional): A dictionary of key-value pairs that will be included
                with this measurement.  These values will be merged with / override any top-level
                tags that were specified when this class was instantiated.

        Returns:
            str
        """
        if isinstance(self.prefix, (str, unicode)):
            prefix = str(self.prefix).strip('.')
            metric = prefix + '.' + str(metric)

        tagset = []
        tags = deepcopy(self.tags)

        if not isinstance(tags, dict):
            tags = {}

        if isinstance(additional_tags, dict):
            tags.update(additional_tags)

        for k, v in tags.items():
            v = str(v)
            v = v.replace('://', '_')
            v = re.sub(TAG_VALUE_REPLACE, '_', v)

            tagset.append('{0}={1}'.format(str(k), v))

        if len(tagset):
            return str(metric) + ',' + ','.join(sorted(tagset))
        else:
            return str(metric)

    def increment(self, metric, value=1, rate=1.0, tags=None):
        """
        Increment the named metric by a given amount.

        Args:
            metric (str): The metric to make an observation for.

            value (int): The amount to increment the metric by.

            rate (float): Sample rate; values less than 1.0 are the probability that the
                observation will be made and not discarded.

            tags (dict, optional): Additional tags to help specify this observation.

        Returns:
            None
        """
        if self.enabled:
            self._statsd.incr(self.get_metric_name(metric, tags), value, rate=rate)

    def decrement(self, metric, value=1, rate=1.0, tags=None):
        """
        Decrement the named metric by a given amount.

        Args:
            metric (str): The metric to make an observation for.

            value (int): The amount to decrement the metric by.

            rate (float): Sample rate; values less than 1.0 are the probability that the
                observation will be made and not discarded.

            tags (dict, optional): Additional tags to help specify this observation.

        Returns:
            None
        """
        if self.enabled:
            self._statsd.decr(self.get_metric_name(metric, tags), value, rate=rate)

    def timing(self, metric, milliseconds, rate=1.0, tags=None):
        """
        Submit a timing value for a metric.

        Args:
            metric (str): The metric to make an observation for.

            milliseconds (int): The time, in milliseconds, that the observation is associated with.

            rate (float): Sample rate; values less than 1.0 are the probability that the
                observation will be made and not discarded.

            tags (dict, optional): Additional tags to help specify this observation.

        Returns:
            None
        """
        if self.enabled:
            self._statsd.timing(self.get_metric_name(metric, tags),
                                milliseconds,
                                rate=rate)

    def gauge(self, metric, value, delta=False, rate=1.0, tags=None):
        """
        Specify a varying value (non-monotomic) for a metric.

        Args:
            metric (str): The metric to make an observation for.

            value (float): The value to set the metric to, or adjust the existing value by.

            delta (bool): Whether ``value`` is an absolute measurement (False) or relative to the
                last observation (True).

            rate (float): Sample rate; values less than 1.0 are the probability that the
                observation will be made and not discarded.

            tags (dict, optional): Additional tags to help specify this observation.

        Returns:
            None
        """
        if self.enabled:
            self._statsd.gauge(self.get_metric_name(metric, tags),
                               value,
                               rate=rate,
                               delta=delta)


default = Stats(enabled=True)


def enable():
    """
    Enable the default global statistics collector.
    """
    global default
    default.enable()


def disable():
    """
    Disable the default global statistics collector.
    """
    global default
    default.disable()


def configure(host=None, port=None, prefix=None, tags=None):
    """
    Configure the default global statistics collector.

    See :class:`Stats`
    """
    global default
    default = Stats(**compact({
        'host': host,
        'port': port,
        'prefix': prefix,
        'tags': tags,
    }))


def increment(*args, **kwargs):
    """
    See: :func:`Stats.increment`
    """
    global default
    default.increment(*args, **kwargs)


def decrement(*args, **kwargs):
    """
    See: :func:`Stats.decrement`
    """
    global default
    default.decrement(*args, **kwargs)


def timing(*args, **kwargs):
    """
    See: :func:`Stats.timing`
    """
    global default
    default.timing(*args, **kwargs)


def gauge(*args, **kwargs):
    """
    See: :func:`Stats.gauge`
    """
    global default
    default.gauge(*args, **kwargs)


class time(object):  # noqa
    def __init__(self, metric, rate=1.0, tags=None):
        self.metric_name = metric
        self.rate = rate
        self.tags = tags

    def __call__(self, view_func):
        def wrap(*args, **kwargs):
            self.__enter__()
            rv = view_func(*args, **kwargs)
            self.__exit__()
            return rv

        return wrap

    def __enter__(self):
        self._block_time_start = datetime.datetime.now()
        return self

    def __exit__(self, *args):
        if self.metric_name and self._block_time_start:
            global default
            delta = datetime.datetime.now() - self._block_time_start
            delta_ms = (delta.total_seconds() * 1000.0)
            default.timing(
                self.metric_name,
                delta_ms,
                rate=self.rate,
                tags=self.tags
            )

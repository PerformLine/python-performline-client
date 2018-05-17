from __future__ import absolute_import
from time import sleep
from unittest import TestCase
from statsdmock import StatsdMockServer
from . import Stats
from .. import stats

server = StatsdMockServer()
server.start()


class StatsTest(TestCase):
    def setUp(self):
        stats.enable()

    def tearDown(self):
        stats.disable()

    def test_stats_global(self):
        instance = stats
        stats.configure()
        prefix = ''

        instance.increment('incr-1')  # 1
        server.wait('%sincr-1' % prefix, n=1, timeout_msec=500)

        instance.increment('incr-2')  # 1
        instance.increment('incr-2')  # 2
        instance.decrement('incr-2')  # 1
        server.wait('%sincr-2' % prefix, n=3, timeout_msec=500)

        instance.increment('incr-3', 3)  # 3
        server.wait('%sincr-3' % prefix, n=1, timeout_msec=500)

        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['value'], '3')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['rate'], 1.0)

    def test_stats_tags(self):
        instance = stats
        prefix = 'test.1.'
        stats.configure(prefix=prefix, tags={
            't1': '123',
            't2': 'http://test:1234',
            't3': 'x=y',
            't4': 'x,,,y',
        })

        tag_suffix = ',t1=123,t2=http_test_1234,t3=x_y,t4=x___y'

        instance.gauge('gauge-1', 3)
        instance.gauge('gauge-2', 4)
        instance.gauge('gauge-3', 5)

        server.wait('%sgauge-1%s' % (prefix, tag_suffix), n=1, timeout_msec=500)
        server.wait('%sgauge-2%s' % (prefix, tag_suffix), n=1, timeout_msec=500)
        server.wait('%sgauge-3%s' % (prefix, tag_suffix), n=1, timeout_msec=500)

        self.assertEqual(server.metrics['%sgauge-1%s' % (prefix, tag_suffix)][0]['value'], '3')
        self.assertEqual(server.metrics['%sgauge-1%s' % (prefix, tag_suffix)][0]['type'], 'gauge')
        self.assertEqual(server.metrics['%sgauge-1%s' % (prefix, tag_suffix)][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sgauge-2%s' % (prefix, tag_suffix)][0]['value'], '4')
        self.assertEqual(server.metrics['%sgauge-2%s' % (prefix, tag_suffix)][0]['type'], 'gauge')
        self.assertEqual(server.metrics['%sgauge-2%s' % (prefix, tag_suffix)][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sgauge-3%s' % (prefix, tag_suffix)][0]['value'], '5')
        self.assertEqual(server.metrics['%sgauge-3%s' % (prefix, tag_suffix)][0]['type'], 'gauge')
        self.assertEqual(server.metrics['%sgauge-3%s' % (prefix, tag_suffix)][0]['rate'], 1.0)

    def test_stats_global_prefix(self):
        instance = stats
        prefix = 'test.1.'
        stats.configure(prefix=prefix)

        instance.increment('incr-1')  # 1
        server.wait('%sincr-1' % prefix, n=1, timeout_msec=500)

        instance.increment('incr-2')  # 1
        instance.increment('incr-2')  # 2
        instance.decrement('incr-2')  # 1
        server.wait('%sincr-2' % prefix, n=3, timeout_msec=500)

        instance.increment('incr-3', 3)  # 3
        server.wait('%sincr-3' % prefix, n=1, timeout_msec=500)

        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['value'], '3')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['rate'], 1.0)

    def test_stats_instance(self):
        prefix = 'test.1.'
        instance = Stats(prefix=prefix)

        instance.increment('incr-1')  # 1
        server.wait('%sincr-1' % prefix, n=1, timeout_msec=500)

        instance.increment('incr-2')  # 1
        instance.increment('incr-2')  # 2
        instance.decrement('incr-2')  # 1
        server.wait('%sincr-2' % prefix, n=3, timeout_msec=500)

        instance.increment('incr-3', 3)  # 3
        server.wait('%sincr-3' % prefix, n=1, timeout_msec=500)

        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['value'], '3')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['rate'], 1.0)

    def test_stats_instance_prefix(self):
        prefix = 'test.1.'
        instance = Stats(prefix=prefix)

        instance.increment('incr-1')  # 1
        server.wait('%sincr-1' % prefix, n=1, timeout_msec=500)

        instance.increment('incr-2')  # 1
        instance.increment('incr-2')  # 2
        instance.decrement('incr-2')  # 1
        server.wait('%sincr-2' % prefix, n=3, timeout_msec=500)

        instance.increment('incr-3', 3)  # 3
        server.wait('%sincr-3' % prefix, n=1, timeout_msec=500)

        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-1' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['value'], '1')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-2' % prefix][0]['rate'], 1.0)

        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['value'], '3')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['type'], 'counter')
        self.assertEqual(server.metrics['%sincr-3' % prefix][0]['rate'], 1.0)

    def test_stats_get_metric_with_tags(self):
        self.assertEqual(stats.default.get_metric_name('stat-1'), 'stat-1')

        self.assertEqual(stats.default.get_metric_name('stat-1', {
            'xyzkey': 'value1',
            'abckey': 'value2',
        }), 'stat-1,abckey=value2,xyzkey=value1')

    def test_stats_with_time(self):
        instance = stats
        stats.configure()

        with instance.time('timer-1'):
            sleep(1)

        server.wait('timer-1', n=1, timeout_msec=1100)
        self.assertTrue(float(server.metrics['timer-1'][0]['value']) > 1000.0)
        self.assertEqual(server.metrics['timer-1'][0]['type'], 'timer')
        self.assertEqual(server.metrics['timer-1'][0]['rate'], 1.0)

    @stats.time('timer-2')
    def sleeper(self):
        sleep(2)

    def test_stats_with_time_as_decorator(self):
        self.sleeper()
        server.wait('timer-2', n=1, timeout_msec=2100)
        self.assertTrue(float(server.metrics['timer-2'][0]['value']) > 2000.0)
        self.assertEqual(server.metrics['timer-2'][0]['type'], 'timer')
        self.assertEqual(server.metrics['timer-2'][0]['rate'], 1.0)

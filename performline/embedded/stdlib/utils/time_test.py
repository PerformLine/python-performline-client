# flake8: noqa
from __future__ import absolute_import
from unittest import TestCase
from .time import Time
from datetime import datetime, timedelta, date
from dateutil import tz


class UtilsTimeTest(TestCase):
    def test_string_to_time(self):
        ns_1h45t         = (60*60*1e9) + (45*60*1e9)
        ns_3y4m27d18h17t11s933l174u42n = long(
            int(3*365*24*60*60*1e9) +
            int(4*30*24*60*60*1e9) +
            int(27*24*60*60*1e9) +
            int(18*60*60*1e9) +
            int(17*60*1e9) +
            int(11*1e9) +
            int(933*1e6) +
            int(174*1e3) +
            int(42)
        )

        self.assertEqual(365*24*60*60*1e9, int(Time.from_pandas_string('1A')))
        self.assertEqual(365*24*60*60*1e9, int(Time.from_pandas_string('1Y')))
        self.assertEqual(365*24*60*60*1e9, int(Time.from_pandas_string('1 year')))
        self.assertEqual(365*24*60*60*1e9, int(Time.from_pandas_string('1 years')))
        self.assertEqual(365*24*60*60*1e9, int(Time.from_pandas_string('1 yr')))
        self.assertEqual(365*24*60*60*1e9, int(Time.from_pandas_string('1 yrs')))

        self.assertEqual(30*24*60*60*1e9,  int(Time.from_pandas_string('1M')))
        self.assertEqual(30*24*60*60*1e9,  int(Time.from_pandas_string('1month')))
        self.assertEqual(30*24*60*60*1e9,  int(Time.from_pandas_string('1 MONTHS')))

        self.assertEqual(24*60*60*1e9,     int(Time.from_pandas_string('1D')))
        self.assertEqual(24*60*60*1e9,     int(Time.from_pandas_string('1 DAY')))
        self.assertEqual(24*60*60*1e9,     int(Time.from_pandas_string('1 days')))

        self.assertEqual(60*60*1e9,        int(Time.from_pandas_string('1H')))
        self.assertEqual(60*60*1e9,        int(Time.from_pandas_string('1HR')))
        self.assertEqual(60*60*1e9,        int(Time.from_pandas_string('1hrs')))
        self.assertEqual(60*60*1e9,        int(Time.from_pandas_string('1 hour')))
        self.assertEqual(60*60*1e9,        int(Time.from_pandas_string('1 hours')))

        self.assertEqual(60*1e9,           int(Time.from_pandas_string('1T')))
        self.assertEqual(60*1e9,           int(Time.from_pandas_string('1min')))
        self.assertEqual(60*1e9,           int(Time.from_pandas_string('1 mins')))
        self.assertEqual(60*1e9,           int(Time.from_pandas_string('1 MINUTE')))
        self.assertEqual(60*1e9,           int(Time.from_pandas_string('1MINUTES')))

        self.assertEqual(1e9,              int(Time.from_pandas_string('1S')))
        self.assertEqual(1e9,              int(Time.from_pandas_string('1 sec')))
        self.assertEqual(1e9,              int(Time.from_pandas_string('1 secs')))
        self.assertEqual(1e9,              int(Time.from_pandas_string('1 SECOND')))
        self.assertEqual(1e9,              int(Time.from_pandas_string('1 seconds')))

        self.assertEqual(1e6,              int(Time.from_pandas_string('1L')))
        self.assertEqual(1e6,              int(Time.from_pandas_string('1ms')))

        self.assertEqual(1e3,              int(Time.from_pandas_string('1U')))
        self.assertEqual(1e3,              int(Time.from_pandas_string('1US')))

        self.assertEqual(1,                int(Time.from_pandas_string('1N')))
        self.assertEqual(1,                int(Time.from_pandas_string('1 ns')))

        self.assertEqual(ns_1h45t, int(Time.from_pandas_string('1H45T')))
        self.assertEqual(
            ns_3y4m27d18h17t11s933l174u42n,
            long(int(Time.from_pandas_string('3A 4M 27D 18H 17T 11S 933L 174U 42N')))
        )

        self.assertEqual(ns_1h45t, int(Time('1H45T')))
        self.assertEqual(
            ns_3y4m27d18h17t11s933l174u42n,
            long(int(Time('3A 4M 27D 18H 17T 11S 933L 174U 42N')))
        )

        self.assertEqual(
            ns_3y4m27d18h17t11s933l174u42n,
            long(int(Time('3Y 4M 27D 18H 17T 11S 933L 174U 42N')))
        )

    def test_relative_time(self):
        base = datetime(2006, 1, 2, 15, 04, 05, 999999, tz.gettz('MST'))
        tm = Time(base)
        self.assertEqual(tm.total_seconds(), 1136239445)
        self.assertEqual(int(tm), 1136239445999999000)

        for pandas_tm, kwargs in [
            ('1D',                    { 'days': -1 }),
            ('1D 2H',                 { 'days': -1, 'hours': -2 }),
            ('366D',                  { 'days': -366 }),
            ('1Y 1D',                 { 'days': -366 }),
            ('3Y 4M 27D 18H 17T 11S', { 'days': -1242, 'hours': -18, 'minutes': -17, 'seconds': -11 }),
        ]:
            self.assertEqual((base + timedelta(**kwargs)), (tm - pandas_tm).as_datetime())

    def test_parse_datetime(self):
        now = datetime.utcnow()

        self.assertIsNotNone(Time().as_datetime())
        self.assertEqual(now.isoformat() + '+00:00', Time(now).isoformat())
        self.assertEqual("2006-01-02T00:00:00+00:00", Time(date(2006, 1, 2)).isoformat())

    def test_parse_string(self):
        base = datetime(2006, 1, 2, 15, 04, 05, 0, tz.gettz('MST'))

        self.assertEqual('3A4M27D',       Time('3A4M27D').freq)
        self.assertEqual('3A4M27D',       Time('3A 4M 27D').freq)
        self.assertEqual('3A4M27D',       Time('3Y 4M 27D').freq)
        self.assertEqual('1N',            Time('1N').freq)
        self.assertEqual(1,               int(Time('1N')))
        self.assertEqual(1000,            int(Time('1000N')))
        self.assertEqual('1D',            Time('86400S').freq)
        self.assertEqual('1A',            Time('525600T').freq)
        self.assertEqual('1A',            Time('525600T').convert_to('A'))
        self.assertEqual('12M5D',         Time('525600T').convert_to('M'))
        self.assertEqual('525600T',       Time('525600T').convert_to('T'))
        self.assertEqual('31536000S',     Time('525600T').convert_to('S'))
        self.assertEqual('1136239445S',   Time(base).convert_to('S'))
        self.assertEqual('13150D22H4T5S', Time(base).convert_to('D'))
        self.assertEqual('36A10D22H4T5S', Time(base).convert_to('A'))

    def test_from_converters(self):
        self.assertEqual(1,                    Time.from_nanoseconds(1))
        self.assertEqual(2e3,                  Time.from_microseconds(2))
        self.assertEqual(4e6,                  Time.from_milliseconds(4))
        self.assertEqual(8e9,                  Time.from_seconds(8))
        self.assertEqual(60*16e9,              Time.from_minutes(16))
        self.assertEqual(60*60*32e9,           Time.from_hours(32))
        self.assertEqual(64*24*60*60*1e9,      Time.from_days(64))
        self.assertEqual(128*30*24*60*60*1e9,  Time.from_months(128))
        self.assertEqual(256*365*24*60*60*1e9, Time.from_years(256))

    def test_to_converters(self):
        self.assertEqual(2,   Time.to_microseconds(2e3))
        self.assertEqual(4,   Time.to_milliseconds(4e6))
        self.assertEqual(8,   Time.to_seconds(8e9))
        self.assertEqual(16,  Time.to_minutes(16*60*1e9))
        self.assertEqual(32,  Time.to_hours(32*60*60*1e9))
        self.assertEqual(64,  Time.to_days(64*24*60*60*1e9))
        self.assertEqual(128, Time.to_months(128*30*24*60*60*1e9))
        self.assertEqual(256, Time.to_years(256*365*24*60*60*1e9))

import logging
import unittest

from unittest.mock import MagicMock

import muselog
from muselog.datadog import DataDogUdpHandler


class SetupLoggingTestCase(unittest.TestCase):

    def test_defaults(self):
        logging.getLogger().setLevel(logging.INFO)
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.INFO)

        muselog.setup_logging()

        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.WARNING)

    def test_custom_log_level(self):
        muselog.setup_logging(root_log_level=logging.CRITICAL)
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.CRITICAL)

    def test_module_log_levels(self):
        muselog.setup_logging(module_log_levels={"muselog": logging.DEBUG,
                                                 "testing": logging.ERROR,
                                                 "testing.child": logging.CRITICAL,
                                                 "string": "INFO"})
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.WARNING)
        self.assertEqual(logging.getLogger("muselog").getEffectiveLevel(), logging.DEBUG)
        self.assertEqual(logging.getLogger("testing").getEffectiveLevel(), logging.ERROR)
        self.assertEqual(logging.getLogger("testing.child").getEffectiveLevel(), logging.CRITICAL)
        self.assertEqual(logging.getLogger("string").getEffectiveLevel(), logging.INFO)


class DataDogTestLoggingTestCase(unittest.TestCase):

    def setUp(self):
        self.handler = h = DataDogUdpHandler(host="127.0.0.1", port=10518)
        self.logger = l = logging.getLogger()

        h.send = MagicMock(name='send')
        l.setLevel(logging.INFO)
        l.addHandler(self.handler)

    def tearDown(self):
        self.logger.removeHandler(self.handler)
        self.handler.close()

    def test_datadog_handler_called(self):
        self.logger.info("Testing handler 1 2 3")
        h = self.handler
        self.assertEqual(True, h.send.called)

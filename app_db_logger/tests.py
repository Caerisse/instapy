# encoding: utf-8
from __future__ import unicode_literals
import logging
from django.contrib.admin import AdminSite
from django.test import TestCase
from app_db_logger.admin import StatusLogAdmin
from .models import StatusLog


class TestDbLogger(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('db_logger')
        self.status_log_admin = StatusLogAdmin(StatusLog, AdminSite())

    def __test_log_aux(self, msg, fn, level):
        fn(msg)
        log_queryset = StatusLog.objects.filter(msg=msg)
        self.assertEqual(log_queryset.count(), 1)
        log = log_queryset.get()
        self.assertEqual(level, log.level)
        self.assertIsNone(log.trace)
        return log

    def test_log(self):
        log = self.__test_log_aux('Debug Message - test_message', self.logger.debug, logging.DEBUG)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: green;">Debug Message - test_message</span>')

        log = self.__test_log_aux('Info Message - test_message', self.logger.info, logging.INFO)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: yellow;">Info Message - test_message</span>')

        log = self.__test_log_aux('Warning Message - test_message', self.logger.warning, logging.WARNING)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: orange;">Warning Message - test_message</span>')

        log = self.__test_log_aux('Error Message - test_message', self.logger.error, logging.ERROR)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: red;">Error Message - test_message</span>')

        log = self.__test_log_aux('Fatal Message - test_message', self.logger.fatal, logging.FATAL)
        self.assertEqual(self.status_log_admin.colored_msg(log),
                         '<span style="color: red;">Fatal Message - test_message</span>')
        self.assertEqual(self.status_log_admin.traceback(log), '<pre><code></code></pre>')

    def test_exception(self):
        exception_message = 'Exception Message'
        try:
            raise Exception(exception_message)
        except Exception as e:
            self.logger.exception(e)

        log_queryset = StatusLog.objects.filter(msg=exception_message)
        self.assertEqual(log_queryset.count(), 1)
        log = log_queryset.get()
        self.assertEqual(logging.ERROR, log.level)
        self.assertIsNotNone(log.trace)

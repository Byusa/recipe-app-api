"""
Test custom Django management commands.
"""
from unittest.mock import patch  # mock the behavior of the DB
# possible error we might get when we use a non ready DB
from psycopg2 import OperationalError as Psycopg2Error

# allow to simulate the code we are test
from django.core.management import call_command
from django.db.utils import OperationalError  # another error
from django.test import SimpleTestCase  # simpleTestCase for no DB


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationError."""
        # first two times raise Psycopg2Error
        # then the next 3 times we raise OperationalError
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(database=['default'])

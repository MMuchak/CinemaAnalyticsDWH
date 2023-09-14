import unittest
from unittest.mock import patch, Mock
from airflow.models import DagBag
from ..dags.postgresql_to_hive_dag import *

class TestPostgresToHiveDag(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the DAG once for all tests
        cls.dagbag = DagBag()

    def test_dag_loaded(self):
        """Ensure the DAG is loaded."""
        dag = self.dagbag.get_dag(dag_id='postgresql_to_hive_incremental')
        self.assertDictEqual(self.dagbag.import_errors, {})
        self.assertIsNotNone(dag)

    def test_default_args(self):
        """Ensure all default_args are correctly set."""
        dag = self.dagbag.get_dag(dag_id='postgresql_to_hive_incremental')
        self.assertEqual(dag.default_args['retries'], 1)

    @patch("dags.postgresql_to_hive_dag.send_email")
    def test_on_failure_callback(self, mock_send_email):
        """Ensure that the on_failure_callback sends an email."""
        on_failure_callback({'exception': Exception("Mocked error")})
        mock_send_email.assert_called()

    @patch("dags.postgresql_to_hive_dag.PostgresHook")
    @patch("dags.postgresql_to_hive_dag.HiveCliHook")
    @patch("pandas.DataFrame.to_csv")
    def test_transfer_table(self, mock_to_csv, mock_hive_hook, mock_postgres_hook):
        """Test the transfer_table function with mock data."""
        mock_postgres_hook.return_value.get_pandas_df.return_value = Mock()
        mock_postgres_hook.return_value.get_first.return_value = (1, )
        mock_hive_hook.return_value.get_first.return_value = (1, )
        # This should complete without raising any exceptions
        transfer_table("UserDim", ti=Mock())

    @patch("dags.postgresql_to_hive_dag.PostgresHook")
    @patch("dags.postgresql_to_hive_dag.HiveCliHook")
    @patch("pandas.DataFrame.to_csv")
    def test_transfer_table_mismatch(self, mock_to_csv, mock_hive_hook, mock_postgres_hook):
        """Test the transfer_table function when counts do not match."""
        mock_postgres_hook.return_value.get_pandas_df.return_value = Mock()
        mock_postgres_hook.return_value.get_first.side_effect = [(1, ), (2, )]
        mock_hive_hook.return_value.get_first.return_value = (1, )
        with self.assertRaises(ValueError):
            transfer_table("UserDim", ti=Mock())

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, Mock
from airflow.models import DagBag
from ..dags.users_oltp_to_dwh_dag import evaluate_users_quality_checks

class TestUsersEtlDag(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the DAG once for all tests in this scenario
        cls.dagbag = DagBag()

    def test_dag_loaded(self):
        """Ensure the DAG is loaded."""
        dag = self.dagbag.get_dag(dag_id='etl_users_oltp_to_dwh')
        self.assertDictEqual(self.dagbag.import_errors, {})
        self.assertIsNotNone(dag)

    def test_default_args(self):
        """Ensure all default_args are correctly set."""
        dag = self.dagbag.get_dag(dag_id='etl_users_oltp_to_dwh')
        self.assertEqual(dag.default_args['retries'], 1)

    def test_task_order(self):
        """Ensure tasks are ordered correctly."""
        dag = self.dagbag.get_dag(dag_id='etl_users_oltp_to_dwh')
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(task_ids, ['extract_users', 'data_quality_check'])

    @patch("airflow.hooks.postgres_hook.PostgresHook")
    def test_data_quality_checks_pass(self, mock_hook):
        """Test the data quality checks pass with mock data."""
        mock_hook.return_value.get_first.side_effect = [
            (True,),  # is_unique
            (0,)     # null_count
        ]
        # The function should complete successfully with no exceptions
        evaluate_users_quality_checks(ti=Mock())

    @patch("airflow.hooks.postgres_hook.PostgresHook")
    def test_data_quality_checks_fail(self, mock_hook):
        """Test the data quality checks fail with mock data."""
        mock_hook.return_value.get_first.side_effect = [
            (False,),  # not unique
            (10,)      # simulating 10 null values found
        ]
        with self.assertRaises(ValueError):
            evaluate_users_quality_checks(ti=Mock())

    # Test the email sending on failure (using PythonOperator's behavior)
    @patch("dags.users_oltp_to_dwh_dag.send_email")
    @patch("airflow.hooks.postgres_hook.PostgresHook")
    def test_email_sent_on_failure(self, mock_hook, mock_send_email):
        mock_hook.return_value.get_first.side_effect = [
            (False,),  # not unique
            (10,)      # simulating 10 null values found
        ]
        with self.assertRaises(ValueError):
            evaluate_users_quality_checks(ti=Mock())

        # Ensure email was attempted to be sent
        mock_send_email.assert_called()

if __name__ == '__main__':
    unittest.main()

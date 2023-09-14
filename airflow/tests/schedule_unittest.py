import unittest
from unittest.mock import patch, Mock
from airflow.models import DagBag
from ..dags.schedule_oltp_to_dwh_dag import evaluate_schedule_quality_checks


class TestEtlScheduleDag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the DAG once for all tests in this scenario
        cls.dagbag = DagBag()

    def test_dag_loaded(self):
        """Ensure the DAG is loaded."""
        dag = self.dagbag.get_dag(dag_id='etl_schedule_oltp_to_dwh')
        self.assertDictEqual(self.dagbag.import_errors, {})
        self.assertIsNotNone(dag)

    def test_default_args(self):
        """Ensure all default_args are correctly set."""
        dag = self.dagbag.get_dag(dag_id='etl_schedule_oltp_to_dwh')
        self.assertEqual(dag.default_args['retries'], 1)

    def test_task_order(self):
        """Ensure tasks are ordered correctly."""
        dag = self.dagbag.get_dag(dag_id='etl_schedule_oltp_to_dwh')
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(task_ids, ['extract_sessions', 'data_quality_check'])

    def test_task_dependencies(self):
        """Ensure correct upstream and downstream dependencies."""
        dag = self.dagbag.get_dag(dag_id='etl_schedule_oltp_to_dwh')
        extract_sessions = dag.get_task('extract_sessions')
        upstream_task_ids = list(map(lambda task: task.task_id, extract_sessions.upstream_list))
        self.assertListEqual(upstream_task_ids, [])
        downstream_task_ids = list(map(lambda task: task.task_id, extract_sessions.downstream_list))
        self.assertListEqual(downstream_task_ids, ['data_quality_check'])

    @patch("airflow.hooks.postgres_hook.PostgresHook")
    def test_data_quality_checks_pass(self, mock_hook):
        """Test the data quality checks pass with mock data."""
        mock_hook.return_value.get_first.side_effect = [
            (True,),    # is_unique
            (0,),       # null_count
            (0,)        # negative_seats
        ]
        # The function should complete successfully with no exceptions
        evaluate_schedule_quality_checks()

    @patch("airflow.hooks.postgres_hook.PostgresHook")
    def test_data_quality_checks_fail(self, mock_hook):
        """Test the data quality checks fail with mock data."""
        mock_hook.return_value.get_first.side_effect = [
            (False,),   # not unique
            (10,),      # simulating 10 null values found
            (-5,)       # negative available seats
        ]
        with self.assertRaises(ValueError):
            evaluate_schedule_quality_checks()

    # Test the email sending on failure (using PythonOperator's behavior)
    @patch("schedule_oltp_to_dwh_dag.send_email")
    @patch("airflow.hooks.postgres_hook.PostgresHook")
    def test_email_sent_on_failure(self, mock_hook, mock_send_email):
        with self.assertRaises(ValueError):
            mock_hook.return_value.get_first.side_effect = [
                (False,),
                (10,),
                (-5,)
            ]
            evaluate_schedule_quality_checks()

        # Ensure email was attempted to be sent
        mock_send_email.assert_called()


if __name__ == '__main__':
    unittest.main()

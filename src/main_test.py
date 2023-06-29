import unittest
from .main import VotesProcessor


class MainTest(unittest.TestCase):
    def test_votes_processor_default_state(self):
        VP = VotesProcessor()

        self.assertEqual(VP.input_path, 'input')
        self.assertEqual(VP.output_path, 'output')

    def test_votes_processor_no_such_file_exception(self):
        with self.assertRaises(FileNotFoundError) as context:
            VP = VotesProcessor(input_path='test_input',
                                output_path='test_output')

            self.assertIn('No such file or directory', context.exception)

    def test_votes_processor_path_injection(self):
        VP = VotesProcessor(input_path='test_files/simple',
                            output_path='test_output')

        self.assertEqual(VP.input_path, 'test_files/simple')
        self.assertEqual(VP.output_path, 'test_output')

    def test_legislator_report_simple(self):
        VP = VotesProcessor(input_path='test_files/simple')
        report = VP.generate_legislator_report()

        self.assertEqual(report['num_supported_bills'].sum(), 3)
        self.assertEqual(report['num_opposed_bills'].sum(), 1)
        self.assertEqual(len(report.index), 4)
        self.assertEqual(report['id'].to_list(), [
                         904789, 1603850, 1852382, 904796])

    def test_legislator_report_full(self):
        VP = VotesProcessor()
        report = VP.generate_legislator_report()

        self.assertEqual(report['num_supported_bills'].sum(), 19)
        self.assertEqual(report['num_opposed_bills'].sum(), 19)
        self.assertEqual(len(report.index), 20)

    def test_legislator_report_correctness(self):
        VP = VotesProcessor(input_path='test_files/correctness')
        report = VP.generate_legislator_report()

        bacon = report.loc[lambda df: df['id'] == 904789]
        bowman = report.loc[lambda df: df['id'] == 1603850]

        self.assertEqual(bacon['num_supported_bills'].item(), 1)
        self.assertEqual(bacon['num_opposed_bills'].item(), 0)
        self.assertEqual(bowman['num_supported_bills'].item(), 0)
        self.assertEqual(bowman['num_opposed_bills'].item(), 1)

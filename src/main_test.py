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

    def test_legislator_report_correctness(self):
        VP = VotesProcessor(input_path='test_files/correctness')
        report = VP.generate_legislator_report()

        bacon = report.iloc[0]
        bowman = report.iloc[1]

        self.assertEqual(bacon['num_supported_bills'].item(), 1)
        self.assertEqual(bacon['num_opposed_bills'].item(), 0)
        self.assertEqual(bowman['num_supported_bills'].item(), 0)
        self.assertEqual(bowman['num_opposed_bills'].item(), 1)

    def test_legislator_report_full(self):
        VP = VotesProcessor()
        report = VP.generate_legislator_report()

        self.assertEqual(report['num_supported_bills'].sum(), 19)
        self.assertEqual(report['num_opposed_bills'].sum(), 19)
        self.assertEqual(len(report.index), 20)

    def test_bill_report_simple(self):
        VP = VotesProcessor(input_path='test_files/simple')
        report = VP.generate_bill_report()

        bill = report.iloc[0]

        self.assertEqual(bill['primary_sponsor'], 'Rep. Don Bacon (R-NE-2)')
        self.assertEqual(bill['supporter_count'], 3)
        self.assertEqual(bill['opposer_count'], 1)

    def test_bill_report_correctness(self):
        VP = VotesProcessor(input_path='test_files/correctness')
        report = VP.generate_bill_report()

        bill = report.iloc[0]

        self.assertEqual(bill['primary_sponsor'], 'Unknown')
        self.assertEqual(bill['supporter_count'], 1)
        self.assertEqual(bill['opposer_count'], 1)

    def test_bill_report_full(self):
        VP = VotesProcessor()
        report = VP.generate_bill_report()

        bill_a = report.iloc[0]
        bill_b = report.iloc[1]

        self.assertEqual(bill_a['primary_sponsor'],
                         'Rep. John Yarmuth (D-KY-3)')
        self.assertEqual(bill_a['supporter_count'], 6)
        self.assertEqual(bill_a['opposer_count'], 13)
        self.assertEqual(bill_b['primary_sponsor'], 'Unknown')
        self.assertEqual(bill_b['supporter_count'], 13)
        self.assertEqual(bill_b['opposer_count'], 6)

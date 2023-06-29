import pandas as pd
from os.path import exists
from os import mkdir

YEA = 1
NAY = 2


class VotesProcessor():
    def __init__(self, input_path='input', output_path='output'):
        self.input_path = input_path
        self.output_path = output_path

        self.bills = pd.read_csv(
            f'{self.input_path}/bills.csv')
        self.legislators = pd.read_csv(
            f'{self.input_path}/legislators.csv')
        self.vote_results = pd.read_csv(
            f'{self.input_path}/vote_results.csv')
        self.votes = pd.read_csv(
            f'{self.input_path}/votes.csv')

    def generate_legislator_report(self, to_disk=False):
        report = pd.DataFrame(
            [self.__process_legislator_row(
                l) for l in self.legislators.to_dict('records')],
            columns=['id', 'name', 'num_supported_bills', 'num_opposed_bills']
        )

        if (to_disk):
            self.__save_report(report, 'legislators-support-oppose-count.csv')

        return report

    def generate_bill_report(self, to_disk=False):
        report = pd.DataFrame(
            [self.__process_bill_row(b)
             for b in self.bills.to_dict('records')],
            columns=['id', 'title', 'supporter_count',
                     'opposer_count', 'primary_sponsor']
        )

        if (to_disk):
            self.__save_report(report, 'bills.csv')

        return report

    def __save_report(self, report, filename):
        if (not exists(self.output_path)):
            mkdir(self.output_path)
        report.to_csv(f'{self.output_path}/{filename}')

    def __process_legislator_row(self, legislator):
        report_row = {'id': legislator['id'], 'name': legislator['name'],
                      'num_supported_bills': 0, 'num_opposed_bills': 0}

        legislator_votes = self.vote_results.loc[lambda df:
                                                 df['legislator_id'] == legislator['id']]

        report_row['num_supported_bills'] = legislator_votes.loc[lambda df: df['vote_type']
                                                                 == YEA]['vote_type'].count()
        report_row['num_opposed_bills'] = legislator_votes.loc[lambda df: df['vote_type']
                                                               == NAY]['vote_type'].count()

        return report_row

    def __process_bill_row(self, bill):
        report_row = {'id': bill['id'], 'title': bill['title'],
                      'supporter_count': 0, 'opposer_count': 0, 'primary_sponsor': 'Unknown'}

        sponsor = self.legislators.loc[lambda df: df['id']
                                       == bill['sponsor_id']]
        if (not sponsor.empty):
            report_row['primary_sponsor'] = sponsor['name'].item()

        vote_id = self.votes.loc[lambda df: df['bill_id']
                                 == bill['id']]['id'].item()
        votes = self.vote_results.loc[lambda df: df['vote_id'] == vote_id]

        supporters = votes.loc[lambda df: df['vote_type'] == YEA]
        opposers = votes.loc[lambda df: df['vote_type'] == NAY]

        report_row['supporter_count'] = len(supporters.index)
        report_row['opposer_count'] = len(opposers.index)

        return report_row


if __name__ == '__main__':
    VP = VotesProcessor()
    legislator_report = VP.generate_legislator_report(to_disk=True)
    bill_report = VP.generate_bill_report(to_disk=True)

    print('==== LEGISLATOR REPORT ====')
    print(legislator_report)

    print('==== BILLS REPORT ====')
    print(bill_report)

    print(
        f'Reports have been saved as .csv files inside folder: {VP.output_path}')

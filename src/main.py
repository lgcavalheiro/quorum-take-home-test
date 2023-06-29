import pandas as pd

YEA = 1
NAY = 2


class VotesProcessor():
    def __init__(self, input_path='input', output_path='output'):
        self.input_path = input_path
        self.output_path = output_path

        self.bills = pd.read_csv(
            f"{self.input_path}/bills.csv", index_col=0)
        self.legislators = pd.read_csv(
            f"{self.input_path}/legislators.csv", index_col=0)
        self.vote_results = pd.read_csv(
            f"{self.input_path}/vote_results.csv", index_col=0)
        self.votes = pd.read_csv(
            f"{self.input_path}/votes.csv", index_col=0)

    def generate_legislator_report(self):
        report = pd.DataFrame(
            columns=['id', 'name', 'num_supported_bills', 'num_opposed_bills'])

        for index, legislator in self.legislators.iterrows():
            report_row = {"id": index, "name": legislator["name"],
                          "num_supported_bills": 0, "num_opposed_bills": 0}

            legislator_votes = self.vote_results.loc[lambda df: df["legislator_id"] == index]

            report_row["num_supported_bills"] = legislator_votes.loc[lambda df: df["vote_type"]
                                                                     == YEA]["vote_type"].count()
            report_row["num_opposed_bills"] = legislator_votes.loc[lambda df: df["vote_type"]
                                                                   == NAY]["vote_type"].count()

            report.loc[len(report)] = report_row

        return report


if __name__ == '__main__':
    pass

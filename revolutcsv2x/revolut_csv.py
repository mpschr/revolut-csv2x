from revolut2.helpers import line2fields


def get_transaction(I,O,XI,XO):
    if not I is None and I != "":
        return float(I)
    if not O is None and O != "":
        return -float(O)
    if not XI is None and XI != "":
        return float(XI)
    if not XO is None and XO != "":
        return -float(XO)


class RevolutCSV(object):
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.header = None

    def read_csv(self):
        with open(self.csv_filename,'r') as revolut_in:
            self.header = line2fields(revolut_in.readline())
            for line in revolut_in:
                yield line

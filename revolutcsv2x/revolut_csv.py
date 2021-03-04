from revolutcsv2x.helpers import line2fields
from revolutcsv2x.constants import EOL, DATE, DESC, OUT, IN, XOUT, XIN, BALANCE, CAT, NOTES
import re


def istransfer(XI,XO):
    if not XI is None and XI != "" and not XO is None and XO != "":
        return False
    return True

def get_transaction(I,O,XI,XO):
    I = I.replace(',','')
    O = O.replace(',','')
    XI = XI.replace(',','')
    XO = XO.replace(',','')
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
        self.currency = None

    def read_csv(self):
        with open(self.csv_filename,'r') as revolut_in:
            self.header = line2fields(revolut_in.readline())
            self.currency = self.currency = re.search('\(.*\)', self.header[OUT]).group()
            for line in revolut_in:
                yield line

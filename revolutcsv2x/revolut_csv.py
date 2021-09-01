from os import remove
from revolutcsv2x.helpers import line2fields
from revolutcsv2x.constants import EOL, DATE, DESC, OUT, IN, XOUT, XIN, BALANCE, CAT, NOTES
import csv
import re


def istransfer(XI,XO):
    if not XI is None and XI != "" and not XO is None and XO != "":
        return False
    return True


def get_transaction(I,O,XI,XO):
    """
    XI and XO  are defined for currency exchanges
    I and O are defined for normal payments and incoming transfers
    if XO/XI & O are defined, a fee was elevated on the currency exchange,
    noted in the field O
    """
    #print(f"I: {I}, O: {O}, XI: {XI}, XO: {XO}")
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

def fix_that_funky_csv(source):
  # be sure to pass a source object that supports
  # iteration (e.g. a file object, or a list of csv text lines)
  # revolut uses ', ' as separator and 
  # doesnt quote correctly the comma when a fee is applied and
  # sometimes has double quotes instead of quotes....

  remove_fee_comma = lambda x: x.replace(', Fee', '- Fee')

  # booking texts containing commatas have a "" before and after 
  replace_quoted_commas = lambda x: re.sub(r'\""', r'\1', x)[0]
  replace_funky_quotes = lambda x: x.replace('""','"')

  # replace that disturbing comma for the thousnd markers
  replace_1k_comma = lambda x: re.subn(r'\"?(\d),(\d\d\d\.\d\d)\"?',r'\1\2', x)[0]


  fake_source = []
  for line in source:
      #print('before',line.strip())
      line = remove_fee_comma(line)
      line = replace_funky_quotes(line)
      line = replace_1k_comma(line)
      fake_source.append(line)
      #print('after ',line)

  return csv.reader(fake_source, delimiter = ',',  skipinitialspace=True, dialect='excel')


  #return csv.reader((line.remove_fee_comama(line).replace(', ', ',').replace_funky_quotes() for line in source), delimiter=',')

  
class RevolutCSV(object):
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.header = None
        self.currency = None

    def read_csv(self):
        for line in fix_that_funky_csv(open(self.csv_filename,'r')):
            line = [x.strip() for x in line]
            if self.header is None:
                self.header = line
                self.currency = self.currency = re.search('\(.*\)', self.header[OUT]).group()
            else:
                yield line


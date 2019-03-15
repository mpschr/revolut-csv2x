import re

from revolutcsv2x.helpers import indexed_fields, line2fields
from revolutcsv2x.revolut_csv import RevolutCSV, get_transaction, istransfer
from datetime import datetime, date
import mt940_writer as mt940


DATE,DESC,OUT,IN,XOUT,XIN,BALANCE,CAT,NOTES=[x for x in range(0,9)]
EOL="\n"

now = datetime.now()
today = f"{now.year}-{now.month}-{now.day}"


class FormattedOutput(object):

    #FORMAT = None
    _formatters_ = {}
    FORMAT = None

    def __init__(self):
        if self.FORMAT is None:
            raise Exception("Format CONSTANT Is missing for this format")

    @classmethod
    def factory(cls, desired_format):
        """
        :rtype: FormattedOutput
        """
        pass
        try:
            return cls._formatters_[desired_format]()
        except KeyError:
            raise Exception(f"File format '{desired_format}' is not defined")

    @classmethod
    def register(cls, desired_format):
        def decorator(subclass):
            cls._formatters_[desired_format] = subclass
            subclass.FORMAT = desired_format
            return subclass
        return decorator

    def format_entry(self, **kwargs):
        """
        :rtype: object
        """
        pass

    def create_output(self, revolut_csv: RevolutCSV):
        csv_filename = revolut_csv.csv_filename
        if not '.csv' in csv_filename:
            csv_filename = csv_filename + ".csv"

        self.output_filename = csv_filename.replace('.csv', f'_{today}.{self.FORMAT}')
        return open(self.output_filename, 'w')

    def convert(self, csv: RevolutCSV):
        raise NotImplementedError()


factory = FormattedOutput.factory
register = FormattedOutput.register

@register("qif")
@register("QIF")
class QIF(FormattedOutput):

    #FORMAT = "qif"

    def __init__(self):
        super(QIF, self).__init__()


    def format_entry(self, h, line):
        fields = indexed_fields(h, line2fields(line))
        label = fields[h[DESC]]
        category = fields[h[CAT]]
        date = datetime.strptime(fields[h[DATE]], '%b %d, %Y').strftime('%d/%m/%Y')

        transaction = get_transaction(fields[h[IN]], fields[h[OUT]], fields[h[XIN]], fields[h[XOUT]])
        return EOL.join([
            f"D{date}",
            f"T{transaction}",
            f"P{label}",
            f"LRevolut:{category}",
            "^", ""
        ])

    def convert(self, csv: RevolutCSV):

        revolut_out = self.create_output(csv)

        for line in csv.read_csv():
            formatted_entry = self.format_entry(h=csv.header, line=line)
            revolut_out.write(formatted_entry)

        revolut_out.close()


from decimal import Decimal

@register("STA")
@register("MT940")
@register("mt940")
class MT940(FormattedOutput):

    def __init__(self):
        super(MT940,self).__init__()
        self.currency = None
        self.account = None
        self.closing_balance = None
        self.opening_balance = None

    def convert(self, csv: RevolutCSV):

        revolut_out = self.create_output(csv)

        transactions = []
        for line in csv.read_csv():
            transactions.append(
                self.format_entry(h=csv.header, line=line)
            )
        transactions = transactions[::-1] # reverse order

        statement = mt940.Statement(
            '59716', ## fake
            self.account,
            '1/1',
            self.opening_balance,
            self.closing_balance,
            transactions
        )
        revolut_out.write(str(statement)+EOL)

        revolut_out.close()

    def format_entry(self, h, line):
        fields = indexed_fields(h, line2fields(line))
        label = fields[h[DESC]]
        balance = Decimal(fields[h[BALANCE]])
        transaction_date = datetime.strptime(fields[h[DATE]], '%b %d, %Y').date()

        amount = get_transaction(fields[h[IN]], fields[h[OUT]], fields[h[XIN]], fields[h[XOUT]])
        amount = Decimal(amount)

        if self.currency is None:
            self.currency = re.search('\(.*\)',h[OUT]).group()
            self.account = mt940.Account('DE45500105178431215523','') ## fake account as not available in revolut statement
            self.closing_balance = mt940.Balance(balance, transaction_date, self.currency)

        previous_balance = balance - amount

        self.opening_balance = mt940.Balance(previous_balance, transaction_date, self.currency)

        transfer_type = mt940.TransactionType.transfer if istransfer( fields[h[XIN]], fields[h[XOUT]]) \
                                else mt940.TransactionType.foreign_exchange

        return mt940.Transaction(transaction_date, Decimal(amount), transfer_type, label)






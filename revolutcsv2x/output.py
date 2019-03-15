from revolut2.helpers import indexed_fields, line2fields
from revolut2.revolut_csv import RevolutCSV, get_transaction
from datetime import datetime

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

        revolut_out = self.create_output(csv)

        for line in csv.read_csv():
            formatted_entry = self.format_entry(h=csv.header, line=line)
            revolut_out.write(formatted_entry)

        revolut_out.close()


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



@register("MT940")
@register("mt940")
class MT940(FormattedOutput):

    #format = 'mt940'

    def __init__(self):
        raise NotImplementedError()




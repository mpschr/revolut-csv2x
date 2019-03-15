import sys

from revolut2.output import QIF, RevolutCSV


prog, revolut_csv_filename = sys.argv  # type: (str, str)
print(revolut_csv_filename)

csv = RevolutCSV(revolut_csv_filename)
rqif = QIF()
rqif.convert(csv)

#revolut_qif = revolut_csv_filename.replace('.csv', f'_{today}.{rqif.format}')





import sys

from revolut2.output import RevolutCSV, factory
import logging

handler = logging.StreamHandler()
logger = logging.getLogger('revolut')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if len(sys.argv != 3):
    print("Usage: ./revolutcsv2x.py desired_format input_csv")
prog, desired_format, revolut_csv_filename = sys.argv  # type: (str, str)

csv = RevolutCSV(revolut_csv_filename)
logger.info(f"Reading Revolut CSV-File {csv.csv_filename}")

formatter = factory(desired_format)
logger.info(f"Desired output format: {formatter.FORMAT}")

formatter.convert(csv)
logger.info(f"Output stored in file {formatter.output_filename}")







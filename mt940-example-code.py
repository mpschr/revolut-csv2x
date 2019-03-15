import sys
from datetime import datetime

# assign h indexes to the constants
DATE,DESC,OUT,IN,XOUT,XIN,BALANCE,CAT,NOTES=[x for x in range(0,9)]
EOL="\n"

prog, revolut_csv = sys.argv

now = datetime.now()
today = f"{now.year}-{now.month}-{now.day}"

if not '.csv' in revolut_csv:
    revolut_csv = revolut_csv + ".csv"
revolut_qif = revolut_csv.replace('.csv',f'_{today}.qif')

line2fields = lambda x: [f.rstrip() for f in x.rstrip().split(';')]
indexed_fields = lambda x,y: {x:y for x,y in zip(x,y)} 

def get_transaction(I,O,XI,XO):
    if not I is None and I != "":
        return float(I)
    if not O is None and O != "":
        return -float(O)
    if not XI is None and XI != "":
        return float(XI)
    if not XO is None and XO != "":
        return -float(XO)


def format_entry(h, line):
    fields = indexed_fields(h, line2fields(line))
    label = fields[h[DESC]]
    category = fields[h[CAT]]
    date = datetime.strptime(fields[h[DATE]], '%b %d, %Y').strftime('%m/%d/%Y')


    print(fields)
    transaction = get_transaction(fields[h[IN]], fields[h[OUT]], fields[h[XIN]], fields[h[XOUT]])
    return EOL.join([
        f"D{date}",
        f"T{transaction}",
        f"P{label}",
        f"L{category}",
        "^"
    ])


from mt940gen import gen_mt9

gen_mt9()



with open(revolut_csv,'r') as revolut_in:
    h = line2fields(revolut_in.readline())
    with open(revolut_qif, 'w') as revolut_out:
        revolut_out.writelines(f"!Type:Bank{EOL}")
        for line in revolut_in:
            qif_entry = format_entry(h, line)
            revolut_out.write(qif_entry)


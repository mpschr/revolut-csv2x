indexed_fields = lambda x, y: {x:y for x, y in zip(x, y)}
line2fields = lambda x: [f.strip() for f in x.strip().split(';')]
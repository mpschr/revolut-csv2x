
class Transaction(object):

    def __init__(self, date, amount, transaction_type, narrative, currency_iso, transaction_reference=None,
                 extra_info=None):
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.narrative = narrative
        self.currency_iso = currency_iso
        self.transaction_reference = transaction_reference
        self.extra_info = extra_info
        self.details = None

    def add_details(self, **kwargs):
        self.details = TransactionDetails(**kwargs)

    def __str__(self):
        return '{value_date}{entry_date}{category}{currency_short}{amount}{type_code}{narrative}'.format(
            value_date=self.date.strftime('%y%m%d'),
            entry_date=self.date.strftime('%m%d'),
            category='C' if self.amount >= 0 else 'D',
            currency_short=self.currency_iso[3],
            amount='{:0.2f}'.format(self.amount).replace('.', ',').replace('-', ''),
            type_code=self.transaction_type.value,
            narrative=self.narrative,
        )




class TransactionDetails(object):

    def __init__(self, operation_code, payement_details, beneficiary, beneficiary_id):
        self.operation_code = operation_code
        self.payment_details = payement_details
        self.beneficiary = beneficiary
        self.beneficiary_id = beneficiary_id

    def __str__(self):
        return '{operation_code}'.format(operation_code,
                                         )


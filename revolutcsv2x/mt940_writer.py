# obtained from https://raw.githubusercontent.com/ministryofjustice/mt940-writer/master/mt940_writer.py

from enum import Enum


class TransactionType(Enum):
    miscellaneous = 'NMSC'
    interest_f = 'FINT'
    transfer = 'NTRF'
    brokerage_fee = 'NBRF'
    miscellaneous_f = 'FMSC'
    charges = 'NCHG'
    bill_of_exchange = 'NBOE'
    cash_letters = 'NCLR'
    cheques = 'NCHK'
    collection = 'NCOL'
    commission = 'NCOM'
    direct_debit = 'NDDT'
    documentary_credit = 'NDCR'
    loan_depost = 'NLDP'
    interest = 'NINT'
    dividends = 'NDIV'
    foreign_exchange = 'NFEX'
    eurocheques = 'NECK'
    equivalent_amount = 'NEQA'
    standing_order = 'NSTO'
    returned_item = 'NRTI'
    value_date_adjustment = 'NVDA'
    travellers_cheques = 'NTCK'


class Account(object):

    def __init__(self, account_number, sort_code):
        self.account_number = account_number
        self.sort_code = sort_code

    def __str__(self):
        return '{account_number} {sort_code}'.format(
            account_number=self.account_number,
            sort_code=self.sort_code
        )


class Balance(object):

    def __init__(self, amount, date, currency_code):
        self.amount = amount
        self.date = date
        self.currency_code = currency_code

    def __str__(self):
        return '{category}{date}{currency_code}{amount}'.format(
            category='C' if self.amount >= 0 else 'D',
            date=self.date.strftime('%y%m%d'),
            currency_code=self.currency_code,
            amount='{:0.2f}'.format(self.amount).replace('.', ',').replace('-', '')
        )


class Transaction(object):

    def __init__(self, date, amount, transaction_type, currency_iso,
                 customer_ref=None, bank_ref="", extra_info=""):
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.customer_ref = customer_ref
        self.bank_ref = bank_ref
        self.currency_iso = currency_iso
        self.extra_info = extra_info
        self.details = None

        if self.customer_ref is None:
            self.customer_ref = "NONREF"

        if self.bank_ref != "" and self.bank_ref[0:2] != "//":
            self.bank_ref = "//" + self.bank_ref

    def add_details(self, **kwargs):
        self.details = TransactionDetails(**kwargs)

    def __str__(self):
        return '{value_date}{entry_date}{category}{currency_short}{amount}{type_code}{customer_ref}'.format(
            value_date=self.date.strftime('%y%m%d'),
            entry_date=self.date.strftime('%m%d'),
            category='C' if self.amount >= 0 else 'D',
            currency_short=self.currency_iso[3],
            amount='{:0.2f}'.format(self.amount).replace('.', ',').replace('-', ''),
            type_code=self.transaction_type.value,
            customer_ref=self.customer_ref,
        )

class TransactionDetails(object):

    def __init__(self, operation_code, payement_details, beneficiary, beneficiary_id):
        self.operation_code = operation_code
        self.payment_details = payement_details
        self.beneficiary = beneficiary
        self.beneficiary_id = beneficiary_id

    def __str__(self):
        return '{operation_code}'.format()

class Statement(object):

    def __init__(self, reference_number, account, statement_number,
                 opening_balance, closing_balance, transactions):
        self.reference_number = reference_number
        self.account = account
        self.statement_number = statement_number
        self.opening_balance = opening_balance
        self.closing_balance = closing_balance
        self.transactions = transactions

    def get_lines(self):
        yield ':20:%s' % self.reference_number
        yield ':25:%s' % self.account
        yield ':28C:%s' % self.statement_number
        yield ':60F:%s' % self.opening_balance
        for transaction in self.transactions:
            yield ':61:%s' % transaction
            if not transaction.details is None:
                yield ':86:%s' % transaction.details
        yield ':62F:%s' % self.closing_balance

    def __str__(self):
        return '\n'.join(self.get_lines())
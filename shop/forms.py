from django import forms
from shop.models import MyBill,Category


SELECT_BILL = (
    ('shop rent', 'Shop Rent'),
    ('electricity bill', 'Electricity Bill'),
    ('wifi bill', 'Wifi Bill'),
    ('donation', 'Donation'),
    ('tea bill', 'Tea Bill'),
    ('customer related', 'Customer Related'),
    ('friends related', 'Friends Related'),
    ('others', 'others'),

)

class BillForm(forms.ModelForm):
    billName=forms.CharField(label="Select Bill Type",widget=forms.Select(choices=SELECT_BILL))
    class Meta:
        model = MyBill
        fields = ['billName', 'total']

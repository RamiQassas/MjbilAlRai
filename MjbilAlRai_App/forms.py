# MjbilAlRai_App/forms.py

from django import forms
from .models import Reservation
from decimal import Decimal

class ReservationForm(forms.ModelForm):
    CONCRETE_CHOICES = [
        ('150', 'عيار 150 كغ'),
        ('200', 'عيار 200 كغ'),
        ('250', 'عيار 250 كغ'),
        ('300', 'عيار 300 كغ'),
        ('350', 'عيار 350 كغ'),
        ('400', 'عيار 400 كغ'),
        ('450', 'عيار 450 كغ'),
        ('500', 'عيار 500 كغ'),
    ]

    concrete_type = forms.ChoiceField(
        choices=CONCRETE_CHOICES,
        label="نوع الخرسانة",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'height: 45px;'})
    )

    class Meta:
        model = Reservation
        fields = [
            'customer_name', 'carpenter_name', 'concrete_type', 'concrete_quantity',
            'site_location', 'estimated_distance', 'additional_notes', 'phone_number'
        ]
        labels = {
            'customer_name': 'اسم العميل',
            'carpenter_name': 'اسم النجار',
            'concrete_quantity': 'كمية الخرسانة (متر مكعب)',
            'site_location': 'موقع الصب',
            'estimated_distance': 'المسافة التقديرية (كم)',
            'additional_notes': 'ملاحظات إضافية',
            'phone_number': 'رقم الهاتف',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'carpenter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'concrete_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'site_location': forms.TextInput(attrs={'class': 'form-control'}),
            'estimated_distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control textarea'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FinancialDetailsForm(forms.ModelForm):
    CONCRETE_CHOICES = [
        ('150', 'عيار 150 كغ'),
        ('200', 'عيار 200 كغ'),
        ('250', 'عيار 250 كغ'),
        ('300', 'عيار 300 كغ'),
        ('350', 'عيار 350 كغ'),
        ('400', 'عيار 400 كغ'),
        ('450', 'عيار 450 كغ'),
        ('500', 'عيار 500 كغ'),
    ]

    concrete_type = forms.ChoiceField(
        choices=CONCRETE_CHOICES,
        label="عيار الخرسانة النهائية",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'height: 45px;'})
    )

    is_completed = forms.BooleanField(
        required=False,
        label="تم اكتمال الحجز",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    completion_date = forms.DateField(
        required=False,
        label="تاريخ اكتمال الحجز",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = [
            'price_per_unit', 'discount', 'accountant_notes', 'payments',
            'concrete_quantity', 'concrete_type', 'is_completed', 'completion_date'
        ]
        labels = {
            'price_per_unit': 'السعر للوحدة (دولار أمريكي)',
            'discount': 'الخصم (دولار أمريكي)',
            'accountant_notes': 'ملاحظات المحاسب',
            'payments': 'مجموع الدفعات المدفوعة (دولار أمريكي)',
            'concrete_quantity': 'كمية الخرسانة النهائية (متر مكعب)',
            'concrete_type': 'عيار الخرسانة النهائية',
            'is_completed': 'الحجز مكتمل',
            'completion_date': 'تاريخ اكتمال الحجز',
        }
        widgets = {
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'accountant_notes': forms.Textarea(attrs={'class': 'form-control'}),
            'payments': forms.NumberInput(attrs={'class': 'form-control'}),
            'concrete_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        discount = cleaned_data.get('discount', Decimal(0))
        payments = cleaned_data.get('payments', Decimal(0))
        price_per_unit = cleaned_data.get('price_per_unit', Decimal(0))
        concrete_quantity = cleaned_data.get('concrete_quantity', Decimal(0))

        # تأكيد الحسابات للحقول المالية والتحقق من أن الخصم والمدفوعات لا تتجاوز المبلغ المسموح به
        if price_per_unit and concrete_quantity:
            total_cost = price_per_unit * concrete_quantity
            discounted_cost = total_cost - discount

            if payments > discounted_cost:
                raise forms.ValidationError("قيمة الدفعات لا يمكن أن تتجاوز التكلفة بعد الخصم.")
        return cleaned_data

class PaymentForm(forms.Form):
    payment_amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label="تسجيل دفعة (دولار أمريكي)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        min_value=0,  # لضمان أن الدفعة لا تكون سالبة
    )

    def __init__(self, *args, **kwargs):
        self.remaining_balance = kwargs.pop('remaining_balance', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean_payment_amount(self):
        payment_amount = self.cleaned_data.get('payment_amount')
        if self.remaining_balance is not None and payment_amount > self.remaining_balance:
            raise forms.ValidationError("قيمة الدفعة لا يمكن أن تتجاوز الرصيد المتبقي.")
        return payment_amount

# Generated by Django 5.1.1 on 2024-10-08 16:43

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100, verbose_name='اسم العميل')),
                ('carpenter_name', models.CharField(max_length=100, verbose_name='اسم النجار')),
                ('concrete_type', models.CharField(max_length=100, verbose_name='نوع الخرسانة')),
                ('concrete_quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='كمية الخرسانة (متر مكعب)')),
                ('site_location', models.CharField(max_length=255, verbose_name='موقع الصب')),
                ('estimated_distance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المسافة التقديرية (كم)')),
                ('additional_notes', models.TextField(blank=True, null=True, verbose_name='ملاحظات إضافية')),
                ('phone_number', models.CharField(help_text="يجب إدخال رقم الهاتف بصيغة: '+999999999'. يمكن إدخال ما يصل إلى 15 رقماً.", max_length=15, verbose_name='رقم الهاتف')),
                ('reservation_number', models.CharField(blank=True, max_length=6, unique=True, verbose_name='رقم الحجز')),
                ('is_approved', models.BooleanField(default=False, verbose_name='تمت الموافقة')),
                ('is_rejected', models.BooleanField(default=False, verbose_name='تم الرفض')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='تم التأكيد')),
                ('reservation_date', models.DateField(blank=True, null=True, verbose_name='تاريخ الحجز')),
                ('approval_date', models.DateField(blank=True, null=True, verbose_name='تاريخ الموافقة')),
                ('approval_message', models.TextField(blank=True, null=True, verbose_name='رسالة الموافقة')),
                ('price_per_unit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='السعر للوحدة (دولار أمريكي)')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=10, null=True, verbose_name='الخصم (دولار أمريكي)')),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='إجمالي التكلفة (دولار أمريكي)')),
                ('accountant_notes', models.TextField(blank=True, null=True, verbose_name='ملاحظات المحاسب')),
                ('payments', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=15, verbose_name='مجموع الدفعات المدفوعة')),
                ('remaining_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='المبلغ المتبقي')),
            ],
            options={
                'permissions': [('can_manage_reservations', 'يمكنه إدارة الحجوزات'), ('can_confirm_reservations', 'يمكنه تأكيد الحجوزات'), ('can_access_accountant_pages', 'يمكنه عرض وتعديل التفاصيل المالية'), ('can_edit_financial_details', 'يمكنه تعديل التفاصيل المالية')],
            },
        ),
    ]

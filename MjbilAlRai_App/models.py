# MjbilAlRai_App/models.py

from django.db import models
import uuid
from datetime import date
from django.core.validators import RegexValidator
from decimal import Decimal

class Reservation(models.Model):
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

    STATUS_CHOICES = [
        ('معلق', 'معلق'),
        ('مقبول', 'مقبول'),
        ('مكتمل', 'مكتمل'),
        ('مرفوض', 'مرفوض'),
    ]

    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    carpenter_name = models.CharField(max_length=100, verbose_name="اسم النجار")
    concrete_type = models.CharField(max_length=100, choices=CONCRETE_CHOICES, verbose_name="نوع الخرسانة")
    concrete_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="كمية الخرسانة (متر مكعب)")
    site_location = models.CharField(max_length=255, verbose_name="موقع الصب")
    estimated_distance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المسافة التقديرية (كم)")
    additional_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات إضافية")
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        help_text="يجب إدخال رقم الهاتف بصيغة: '+999999999'. يمكن إدخال ما يصل إلى 15 رقماً.",
        verbose_name="رقم الهاتف"
    )
    reservation_number = models.CharField(max_length=6, unique=True, blank=True, verbose_name="رقم الحجز")
    is_approved = models.BooleanField(default=False, verbose_name="تمت الموافقة")
    is_rejected = models.BooleanField(default=False, verbose_name="تم الرفض")
    is_confirmed = models.BooleanField(default=False, verbose_name="تم التأكيد")
    reservation_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الحجز")
    approval_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الموافقة")
    approval_message = models.TextField(blank=True, null=True, verbose_name="رسالة الموافقة")

    # الحقول المالية الجديدة
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="السعر للوحدة (دولار أمريكي)")
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal(0), verbose_name="الخصم (دولار أمريكي)")
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="إجمالي التكلفة قبل الخصم (دولار أمريكي)")
    accountant_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات المحاسب")
    payments = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0), verbose_name="مجموع الدفعات المدفوعة")
    remaining_balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="المبلغ المتبقي")

    # حقل تاريخ اكتمال الحجز
    completion_date = models.DateField(null=True, blank=True, verbose_name="تاريخ اكتمال الحجز")

    # حقل يوضح ما إذا كان الحجز مكتملًا أم لا
    is_completed = models.BooleanField(default=False, verbose_name="الحجز مكتمل")

    # حقل الحالة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='معلق', verbose_name="حالة الحجز")

    class Meta:
        permissions = [
            ("can_manage_reservations", "يمكنه إدارة الحجوزات"),
            ("can_confirm_reservations", "يمكنه تأكيد الحجوزات"),
            ("can_manage_accountant", "يمكنه إدارة صفحات المحاسب"),
        ]

    def save(self, *args, **kwargs):
        # توليد رقم الحجز الفريد إذا لم يكن موجودًا
        if not self.reservation_number:
            while True:
                reservation_number = str(uuid.uuid4().int)[:6]
                if not reservation_number.startswith('0') and not Reservation.objects.filter(reservation_number=reservation_number).exists():
                    self.reservation_number = reservation_number
                    break

        # تأكد من أنه لا يمكن أن يكون كلا الحقلين 'تمت الموافقة' و 'تم الرفض' True في نفس الوقت
        if self.is_approved and self.is_rejected:
            raise ValueError("لا يمكن أن يكون كلا الحقلين 'تمت الموافقة' و 'تم الرفض' True في نفس الوقت.")

        # تعيين تاريخ الحجز إلى اليوم إذا لم يكن محددًا
        if not self.reservation_date:
            self.reservation_date = date.today()

        # حساب التكلفة الإجمالية قبل الخصم
        if self.price_per_unit and self.concrete_quantity:
            self.total_cost = self.price_per_unit * self.concrete_quantity

        # حساب المبلغ المتبقي بعد الخصم والمدفوعات
        if self.total_cost is not None:
            # المتبقي = التكلفة الإجمالية - الخصم - المدفوعات
            self.remaining_balance = self.total_cost - (self.discount or Decimal(0)) - self.payments

        # إذا كان الحجز مكتملًا ولم يتم تحديد تاريخ اكتمال الحجز، حدد التاريخ إلى اليوم الحالي
        if self.is_completed and not self.completion_date:
            self.completion_date = date.today()

        # إذا لم يكن الحجز مكتملًا، قم بإزالة تاريخ الاكتمال (للحالات التي قد يعود فيها الحجز ليكون غير مكتمل)
        if not self.is_completed:
            self.completion_date = None

        # تحديث حالة الحجز بناءً على الحقول الحالية
        if self.is_approved and not self.is_rejected and not self.is_confirmed and not self.is_completed:
            self.status = 'مقبول'
        elif self.is_completed:
            self.status = 'مكتمل'
        elif self.is_rejected:
            self.status = 'مرفوض'
        else:
            self.status = 'معلق'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.reservation_number}"

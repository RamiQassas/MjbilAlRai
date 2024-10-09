# MjbilAlRai_App/urls.py

from django.urls import path
from . import views  # استيراد جميع العروض من ملف views.py

urlpatterns = [
    # المسارات الأساسية للحجوزات
    path('', views.home, name='home'),  # الصفحة الرئيسية للبحث عن الحجوزات باستخدام رقم الهاتف أو رقم الحجز
    path('new/', views.new_reservation, name='new_reservation'),  # إنشاء حجز جديد
    path('manage/', views.manage_reservations, name='manage_reservations'),  # إدارة الحجوزات (للمسؤولين)
    path('confirm/', views.confirm_reservations, name='confirm_reservations'),  # تأكيد الحجوزات (للمسؤولين)
    path('approve/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),  # قبول حجز معين
    path('reject/<int:reservation_id>/', views.reject_reservation, name='reject_reservation'),  # رفض حجز معين

    # مسارات تسجيل الدخول والخروج
    path('login/', views.login_user, name='login'),  # تسجيل الدخول
    path('logout/', views.logout_user, name='logout'),  # تسجيل الخروج

    # مسارات لعرض حجوزات العملاء
    path('customer_reservations/', views.customer_reservations, name='customer_reservations'),  # عرض الحجوزات للعميل بناءً على رقم الهاتف
    path('export_customer_reservations/', views.export_customer_reservations, name='export_customer_reservations'),  # تصدير حجوزات العميل إلى ملف Excel
    path('export_reservations/', views.export_reservations, name='export_reservations'),  # تصدير قائمة الحجوزات إلى ملف Excel

    # المسارات المتعلقة بالبيانات المالية
    path('accountant_dashboard/', views.accountant_dashboard, name='accountant_dashboard'),  # لوحة المحاسب لعرض الحجوزات المكتملة وإدخال البيانات المالية
    path('update_financial_details/<int:reservation_id>/', views.update_financial_details, name='update_financial_details'),  # تحديث بيانات مالية لحجز
]

from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('student_detail/<int:pk>/', views.student_detail, name='student_detail'),
    path('edit_student/<int:pk>/', views.edit_student, name='edit_student'),
    # path('register/', views.register, name='register'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('add_expense/<int:pk>/', views.add_expense, name='add_expense'),
    path('pay_installment/<int:pk>/', views.pay_installment, name='pay_installment'),
    path('receipt/<int:pk>/', views.receipt, name='receipt'),
    path('report/', views.report, name='report'),
    path('all_reports/', views.all_reports, name='all_reports'),
    path('search/', views.search_student, name='search_student'),
]
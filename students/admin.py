from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)

@admin.register(EducationalStage)
class EducationalStageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'educational_stage', 'academic_year')
    list_filter = ('educational_stage', 'academic_year')
    search_fields = ('name', 'educational_stage__name', 'academic_year__year')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_number', 'age', 'gender', 'date_of_birth')
    list_filter = ('gender', 'classroom__educational_stage', 'classroom__academic_year')
    search_fields = ('name', 'national_number')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('student', 'expense_type', 'amount', 'date')
    list_filter = ('student__classroom__educational_stage', 'student__classroom__academic_year', 'expense_type')
    search_fields = ('student__name',)

@admin.register(Tuition)
class TuitionAdmin(admin.ModelAdmin):
    list_display = ('student', 'installment_number', 'amount', 'receipt_date')
    list_filter = ('student__classroom__educational_stage', 'student__classroom__academic_year')
    search_fields = ('student__name',)
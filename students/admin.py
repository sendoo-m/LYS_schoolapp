from django.contrib import admin
from .models import *

admin.site.site_header = "School App"  # Set the admin site header
admin.site.site_title = "School App"  # Set the admin site title

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
    list_display = ('get_name', 'get_educational_stage')

    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'Name'

    def get_educational_stage(self, obj):
        return obj.educational_stage.name

    get_educational_stage.short_description = 'Educational Stage'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_number', 'age', 'gender', 'date_of_birth')
    list_filter = ('gender', 'classroom__educational_stage')
    search_fields = ('name', 'national_number')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'expense_type', 'amount', 'date')
    list_filter = ('classroom__educational_stage', 'expense_type')
    search_fields = ('student__name',)

    def get_name(self, obj):
        return obj.classroom.name

    get_name.short_description = 'Classroom Name'


@admin.register(Tuition)
class TuitionAdmin(admin.ModelAdmin):
    list_display = ('student', 'installment_number', 'amount', 'receipt_date')
    list_filter = ('student__classroom__educational_stage', )
    search_fields = ('student__name',)

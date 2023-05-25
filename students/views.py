from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Sum
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.db.models import Q


# Create your views here.

def home(request):
    students = Student.objects.all()
    paginator = Paginator(students, 10)  # Display 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'page_obj': page_obj,  # Pass the page_obj variable to the template
    }
    return render(request, 'students/home.html', context)


@login_required
def search_student(request):
    query = request.GET.get('query')
    students = Student.objects.all().order_by('name')

    if query and query.strip():
        students = students.filter(Q(name__icontains=query) | Q(national_number__icontains=query))

    paginator = Paginator(students, 5)  # Display 5 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'query': query,
        'page_obj': page_obj,  # Add this line to include the page_obj in the context
    }
    return render(request, 'students/search_student.html', context)

  

def student_list(request):
    students = Student.objects.all()
    student_list = Student.objects.all()
    paginator = Paginator(student_list, 10) # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Total male students
    total_male_students = Student.objects.filter(gender='M').count()

    # Total female students
    total_female_students = Student.objects.filter(gender='F').count()
  
    context = {
        'total_male_students': total_male_students,
        'total_female_students': total_female_students,
        'students': students,
        'page_obj': page_obj
    }
    return render(request, 'students/student_list.html', context )

@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = Student_edit_Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully!')
            return redirect('students:home')
    else:
        form = Student_edit_Form(instance=student)
    context = {
        'form': form,
        'title': 'Edit Student'
    }
    return render(request, 'students/edit_student_form.html', context)


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('students:home')
    context = {
        'student': student,
    }
    return render(request, 'students/delete_student.html', context)


@never_cache
@login_required
def add_student(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = student_form.save(commit=False)  # Save the student object without committing to the database
            student.save()  # Save the student object to generate an ID
            student_form.save_m2m()  # Save the many-to-many relationships after saving the student
            messages.success(request, 'Student added successfully!')
            return redirect('students:add_student')
    else:
        student_form = StudentForm()
   
    context = {
        'student_form': student_form,
    }
    return render(request, 'students/add_student.html', context)

@never_cache
@login_required
def add_expense(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    students = classroom.students.all()

    if request.method == 'POST':
        expense_type = request.POST['expense_type']
        amount = request.POST['amount']
        date = request.POST['date']

        for student in students:
            Expense.objects.create(student=student, classroom=classroom, expense_type=expense_type, amount=amount, date=date)

        messages.success(request, 'Expenses added successfully!')
        return redirect('add_expense', classroom_id=classroom_id)

    context = {
        'classroom': classroom,
    }

    return render(request, 'students/add_expense.html', context)



@never_cache
@login_required
def pay_installment(request, pk):
    user = request.user
    student = get_object_or_404(Student, pk=pk)
    
    student_name = student.name
    national_number = student.national_number

    if request.method == 'POST':
        installment_form = TuitionForm(request.POST)
        if installment_form.is_valid():
            installment = installment_form.save(commit=False)
            installment.student = student
            installment.user = user  # Set the user attribute to the current user who is logged in
            installment.paid = True
            installment.save()
            messages.success(request, 'Installment paid successfully!')
            return redirect('students:student_detail', pk=pk)
    else:
        installment_form = TuitionForm()

    context = {
        'student': student,
        'student_name': student_name,
        'national_number': national_number,
        'installment_form': installment_form,
    }
    return render(request, 'students/pay_installment.html', context)


def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comments:list')
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form})

def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comment_list.html', {'comments': comments})

@never_cache
@login_required
def receipt(request, pk):
    tuition = get_object_or_404(Tuition, pk=pk)
    student = tuition.student  # Retrieve the student from the tuition object
    installments = Tuition.objects.filter(student=student)
    total_paid = sum(installment.amount for installment in installments if installment.paid)
    classroom = student.classroom.first()  # Retrieve the first classroom for the student
    expenses = Expense.objects.filter(classroom=classroom)
    total_expenses = sum(expense.amount for expense in expenses)
    total_owed = total_expenses - total_paid
    if not tuition.paid:
        messages.warning(request, 'This installment has not been paid yet.')
        return redirect('student_detail', pk=student.pk)  # Use student.pk instead of tuition.student.pk
    else:
        context = {
            'tuition': tuition,
            'installments': installments,
            'total_paid': total_paid,
            'expenses': expenses,
            'total_expenses': total_expenses,
            'total_owed': total_owed,
        }
        return render(request, 'students/receipt.html', context)



@never_cache
@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    installments = Tuition.objects.filter(student=student)
    total_paid = sum(installment.amount for installment in installments if installment.paid)
    classroom = student.classroom.first()  # retrieve the first classroom for the student
    expenses = Expense.objects.filter(classroom=classroom)
    total_expenses = sum(expense.amount for expense in expenses)
    total_owed = total_expenses - total_paid
    context = {
        'student': student,
        'installments': installments,
        'total_paid': total_paid,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'total_owed': total_owed,
    }
    return render(request, 'students/student_detail.html', context)


def report(request):
    # Number of registered students
    registered_students = Student.objects.count()

    # Total installments that have been paid
    total_paid_installments = Tuition.objects.filter(paid=True).count()

    # The total number of students who did not pay
    total_unpaid_students = Student.objects.exclude(installments__paid=True).count()

    # Total male students
    total_male_students = Student.objects.filter(gender='M').count()

    # Total female students
    total_female_students = Student.objects.filter(gender='F').count()

    # Statistics appear for each educational stage
    stages = Classroom.objects.all()
    stage_stats = []
    for stage in stages:
        stage_students = Student.objects.filter(classroom=stage)
        total_stage_students = stage_students.count()
        paid_stage_tuitions = Tuition.objects.filter(student__in=stage_students, paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        unpaid_stage_students = stage_students.exclude(installments__paid=True).count()
        male_stage_students = stage_students.filter(gender='M').count()
        female_stage_students = stage_students.filter(gender='F').count()
        stage_stats.append({
            'stage': stage,
            'total_stage_students': total_stage_students,
            'paid_stage_tuitions': paid_stage_tuitions,
            'unpaid_stage_students': unpaid_stage_students,
            'male_stage_students': male_stage_students,
            'female_stage_students': female_stage_students,
        })

    # Show statistics for all data on the application
    total_tuitions = Tuition.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid_students = Student.objects.filter(installments__paid=True).count()
    total_unpaid_tuitions = Tuition.objects.filter(paid=False).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'registered_students': registered_students,
        'total_paid_installments': total_paid_installments,
        'total_unpaid_students': total_unpaid_students,
        'total_male_students': total_male_students,
        'total_female_students': total_female_students,
        'stage_stats': stage_stats,
        'total_tuitions': total_tuitions,
        'total_paid_students': total_paid_students,
        'total_unpaid_tuitions': total_unpaid_tuitions,
    }

    return render(request, 'students/report.html', context)



from django.db.models import Sum
# كود يعمل بنفس المشكلة
# def all_reports(request):
#     stages = Classroom.objects.all()
#     stage_stats = []

#     for stage in stages:
#         stage_students = Student.objects.filter(classroom=stage)
#         total_stage_students = stage_students.count()

#         paid_stage_tuitions = Tuition.objects.filter(student__in=stage_students, paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
#         unpaid_stage_students = stage_students.exclude(installments__paid=True).count()
#         total_stage_tuitions = stage_students.aggregate(Sum('installments__amount'))['installments__amount__sum'] or 0

#         total_stage_expenses = Expense.objects.filter(classroom=stage).aggregate(Sum('amount'))['amount__sum'] or 0

#         remaining_stage_tuitions = total_stage_tuitions - paid_stage_tuitions
#         # remaining_stage_expenses = total_stage_expenses 
#         remaining_stage_expenses = total_stage_expenses   # تعديل سندوو

#         stage_stats.append({
#             'stage': stage,
#             'total_stage_students': total_stage_students,
#             'total_stage_tuitions': total_stage_tuitions,
#             'paid_stage_tuitions': paid_stage_tuitions,
#             'unpaid_stage_students': unpaid_stage_students,
#             'remaining_stage_tuitions': remaining_stage_tuitions,
#             'total_stage_expenses': total_stage_expenses,
#             'remaining_stage_expenses': remaining_stage_expenses,
#             # 'total_remaining_fees': remaining_stage_tuitions - paid_stage_tuitions + remaining_stage_expenses, # محتاج اظبط عملية الطرح
#             'total_remaining_fees': remaining_stage_expenses - unpaid_stage_students, # تعديل سندوو
#         })

#     context = {
#         'stage_stats': stage_stats,
#     }

#     return render(request, 'students/all_reports.html', context) # نهاية الكود الذي يعمل بنفس المشكله
from django.shortcuts import render
from django.db.models import Sum
from .models import Classroom, Tuition, Student


from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Classroom, Tuition, Student

from django.db.models import Sum

from django.db.models import Sum

# def all_reports(request): الكود يعمل ولكن رقمين فقط لا يظهروا
#     # Overall statistics
#     total_students = Student.objects.count()
#     total_installments_paid = Tuition.objects.filter(paid=True).count()
#     total_fees_due = Tuition.objects.aggregate(total=Sum('amount'))['total'] or 0
#     paid_students = Student.objects.filter(installments__paid=True).distinct().count()
#     unpaid_students = Student.objects.filter(installments__paid=False).distinct().count()
#     total_fees_paid = Tuition.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0
#     total_remaining = total_fees_due - total_fees_paid
    
#     classroom_stats = []  # Define an empty list to hold the classroom statistics
    
#     for classroom in Classroom.objects.all():
#         classroom_students = classroom.student_set.count()
#         classroom_fees_due = Tuition.objects.filter(student__classroom=classroom).aggregate(total=Sum('amount'))['total'] or 0
#         total_paid_students = classroom.student_set.filter(installments__paid=True).count()
#         total_unpaid_students = classroom.student_set.filter(installments__paid=False).count()
#         remaining_tuitions = classroom_fees_due - (Tuition.objects.filter(student__classroom=classroom, paid=True).aggregate(total=Sum('amount')).get('total') or 0)
#         classroom_stat = {
#             'classroom': classroom.name,
#             'total_students': classroom_students,
#             'total_fees_due': classroom_fees_due,
#             'total_paid_students': total_paid_students,
#             'total_unpaid_students': total_unpaid_students,
#             'remaining_tuitions': remaining_tuitions,
#         }
#         classroom_stats.append(classroom_stat)

#     context = {
#         'total_students': total_students,
#         'total_installments_paid': total_installments_paid,
#         'total_fees_due': total_fees_due,
#         'paid_students': paid_students,
#         'unpaid_students': unpaid_students,
#         'total_remaining': total_remaining,
#         'classroom_stats': classroom_stats,
#     }
#     return render(request, 'students/all_reports.html', context)



from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from django.db.models import Sum, Case, When, F, IntegerField

def all_reports(request):
    # Overall statistics
    total_students = Student.objects.count()
    total_installments_paid = Tuition.objects.filter(paid=True).count()
    total_fees_due = Tuition.objects.aggregate(total=Sum('amount'))['total'] or 0
    paid_students = Student.objects.filter(installments__paid=True).distinct().count()
    total_fees_paid = Tuition.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0
    total_remaining = total_fees_due - total_fees_paid

    classroom_stats = []  # Define an empty list to hold the classroom statistics
    
    for classroom in Classroom.objects.all():
        classroom_students = classroom.student_set.count()
        
        classroom_fees_due = Tuition.objects.filter(student__classroom=classroom).aggregate(total=Sum('amount'))['total'] or 0
        classroom_fees_paid = Tuition.objects.filter(student__classroom=classroom, paid=True).aggregate(total=Sum('amount'))['total'] or 0
        remaining_tuitions = classroom_fees_due - classroom_fees_paid
        
        total_paid_students = classroom.student_set.filter(installments__paid=True).count()
        total_unpaid_students = classroom_students - total_paid_students
        
        classroom_stat = {
            'classroom': classroom.name,
            'total_students': classroom_students,
            'total_fees_due': classroom_fees_due,
            'total_paid_students': total_paid_students,
            'total_unpaid_students': total_unpaid_students,
            'remaining_tuitions': remaining_tuitions,
        }
        classroom_stats.append(classroom_stat)

    context = {
        'total_students': total_students,
        'total_installments_paid': total_installments_paid,
        'total_fees_due': total_fees_due,
        'paid_students': paid_students,
        'unpaid_students': total_students - paid_students,
        'total_remaining': total_remaining,
        'classroom_stats': classroom_stats,
    }
    return render(request, 'students/all_reports.html', context)



from django.shortcuts import render
from datetime import date

def generate_daily_report(request):
    report_date = date.today()
    paid_students = Student.objects.filter(installments__paid=True, installments__receipt_date=report_date)
    return render(request, 'students/daily_report.html', {'report_date': report_date, 'paid_students': paid_students})

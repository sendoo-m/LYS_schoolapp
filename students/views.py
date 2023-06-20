from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.db.models import Q
from datetime import date
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When, F, IntegerField
from datetime import timedelta


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
 

# def student_list(request):
#     # Retrieve all students
#     students = Student.objects.all()

#     # Create an instance of the search form
#     search_form = StudentSearchForm(request.GET)

#     # Apply search filter if provided
#     if search_form.is_valid():
#         search_query = search_form.cleaned_data.get('search_query')
#         if search_query:
#             students = students.filter(
#                 Q(name__icontains=search_query) | Q(national_number__icontains=search_query)
#             )

#     # Paginate the student list
#     paginator = Paginator(students, 10)  # Show 10 students per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     # Total male students
#     total_male_students = Student.objects.filter(gender='M').count()

#     # Total female students
#     total_female_students = Student.objects.filter(gender='F').count()
  
#     context = {
#         'total_male_students': total_male_students,
#         'total_female_students': total_female_students,
#         'students': students,
#         'page_obj': page_obj,
#         'search_form': search_form,
#     }
#     return render(request, 'students/student_list.html', context)

def student_list(request):
    # Retrieve all students
    students = Student.objects.all()

    # Create an instance of the search form
    search_form = StudentSearchForm(request.GET)

    # Apply search filter if provided
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        educational_stage = search_form.cleaned_data.get('educational_stage')
        gender = search_form.cleaned_data.get('gender')
        date_of_birth = search_form.cleaned_data.get('date_of_birth')
        classroom = search_form.cleaned_data.get('classroom')

        if search_query:
            students = students.filter(
                Q(name__icontains=search_query) | Q(national_number__icontains=search_query)
            )
        if educational_stage:
            students = students.filter(classroom__educational_stage=educational_stage)
        if gender:
            students = students.filter(gender=gender)
        if date_of_birth:
            students = students.filter(date_of_birth=date_of_birth)
        if classroom:
            students = students.filter(classroom=classroom)

    # Paginate the student list
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Total male students
    total_male_students = students.filter(gender='M').count()

    # Total female students
    total_female_students = students.filter(gender='F').count()

    context = {
        'total_male_students': total_male_students,
        'total_female_students': total_female_students,
        'students': students,
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'students/student_list.html', context)

@never_cache
@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = Student_edit_Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully!')
            return redirect('students:student_list')
    else:
        form = Student_edit_Form(instance=student)
        # print(form.errors)
        
    context = {
        'form': form,
        'title': 'Edit Student',
    }
    return render(request, 'students/edit_student_form.html', context)

@never_cache
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
def confirm_delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('students:home')
    context = {
        'student': student,
    }
    return render(request, 'students/confirm_delete_student.html', context)

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
    total_paid = sum(installment.amount_tuition for installment in installments if installment.paid)
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
def delete_installment(request, pk):
    tuition = get_object_or_404(Tuition, pk=pk)
    
    if request.method == 'POST':
        # Delete the tuition object
        tuition.delete()
    return redirect('students:student_detail', pk=tuition.student.pk)  # Use student.pk instead of tuition.student.pk

@never_cache
@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    installments = Tuition.objects.filter(student=student)
    total_paid = sum(installment.amount_tuition for installment in installments if installment.paid)
    classroom = student.classroom.first()  # retrieve the first classroom for the student
    expenses = Expense.objects.filter(classroom=classroom)
    total_expenses = sum(expense.amount for expense in expenses)
    total_owed = total_expenses - total_paid

    if request.method == 'POST':
        # Assuming you have a form for paying installments with a field named 'payment_amount'
        payment_amount = request.POST.get('payment_amount')
        if payment_amount:
            payment_amount = float(payment_amount)
            # Update the installment as paid
            # Assuming you have a logic to mark an installment as paid, e.g., changing the 'paid' field to True
            # Update the 'total_payments' field in the associated student
            installment = Tuition.objects.create(student=student, amount_tuition=payment_amount, paid=True)
            student.update_total_payments()

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
    total_unpaid_students = Student.objects.exclude(tuitions__paid=True).count()

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
        paid_stage_tuitions = Tuition.objects.filter(student__in=stage_students, paid=True).aggregate(Sum('amount_tuition'))['amount_tuition__sum'] or 0
        unpaid_stage_students = stage_students.exclude(tuitions__paid=True).count()
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
    total_tuitions = Tuition.objects.aggregate(Sum('amount_tuition'))['amount_tuition__sum'] or 0
    total_paid_students = Student.objects.filter(tuitions__paid=True).count()
    total_unpaid_tuitions = Tuition.objects.filter(paid=False).aggregate(Sum('amount_tuition'))['amount_tuition__sum'] or 0

    # Handle form submission and retrieve expenses for the selected stage
    selected_stage = None
    expenses = []
    if request.method == 'GET':
        stage_id = request.GET.get('stage_id')
        if stage_id:
            try:
                selected_stage = Classroom.objects.get(id=stage_id)
                expenses = Expense.objects.filter(classroom=selected_stage)
            except Classroom.DoesNotExist:
                pass

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
        'stages': stages,
        'selected_stage': selected_stage,
        'expenses': expenses,
    }

    return render(request, 'students/report.html', context)




def all_reports(request):
    # Overall statistics
    total_students = Student.objects.count()
    total_installments_paid = Tuition.objects.filter(paid=True).count()
    total_fees_due = Student.objects.aggregate(total_payments=Sum('total_payments'))['total_payments'] or 0
    total_fees_due *= total_students
    paid_students = Student.objects.filter(tuitions__paid=True).distinct().count()
    total_fees_paid = Tuition.objects.filter(paid=True).aggregate(total=Sum('amount_tuition'))['total'] or 0

    classroom_stats = []
    classrooms = Classroom.objects.all()
    for classroom in classrooms:
        total_students_classroom = classroom.student_set.count()
        total_fees_due_classroom = classroom.student_set.aggregate(total_payments=Sum('total_payments'))['total_payments'] or 0
        total_paid_students = classroom.student_set.filter(tuitions__paid=True).count()
        total_unpaid_students = 0  # Set total_unpaid_students initially to 0

        # Update total_unpaid_students if there are unpaid students
        if total_paid_students < total_students_classroom:
            total_unpaid_students = total_students_classroom - total_paid_students

        total_remaining_tuitions = (Expense.objects.filter(classroom=classroom).aggregate(total_expense=Sum('amount'))['total_expense'] or 0) * total_students_classroom
        total_remaining_tuitions -= total_fees_due_classroom

        classroom_stat = {
            'classroom': classroom,
            'total_students': total_students_classroom,
            'total_fees_due': total_fees_due_classroom,
            'total_paid_students': total_paid_students,
            'total_unpaid_students': total_unpaid_students,
            'remaining_tuitions': total_remaining_tuitions,
        }
        classroom_stats.append(classroom_stat)

    # Calculate total_remaining
    total_remaining = sum(classroom['remaining_tuitions'] for classroom in classroom_stats)
    
    # Calculate total_fees_due
    total_fees_due = sum(classroom['total_fees_due'] for classroom in classroom_stats)
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



# get total from student table its good work


# def classroom_details(request, classroom_id):
    
#     classroom = Classroom.objects.get(id=classroom_id)

#     # Calculate total expenses for the classroom
#     total_expenses = Expense.objects.filter(classroom=classroom).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

#     # Get the search query from the request
#     search_query = request.GET.get('search')

#     # Filter students based on the search query
#     if search_query:
#         students = classroom.student_set.filter(Q(name__icontains=search_query) | Q(national_number__icontains=search_query))
#     else:
#         students = classroom.student_set.all()

#     # Paginate the students
#     paginator = Paginator(students, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'classroom': classroom,
#         'page_obj': page_obj,
#         'search_query': search_query,
#         'total_expenses': total_expenses,
#     }

#     return render(request, 'students/classroom_details.html', context)

from django.db.models import Sum

from django.db.models import Sum

def classroom_details(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    expenses = Expense.objects.filter(classroom=classroom)
    total_expenses = expenses.aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

    # Calculate total paid for the classroom
    total_paid = Tuition.objects.filter(student__classroom=classroom, paid=True).aggregate(total=Sum('amount_tuition'))['total'] or 0

    # Calculate total owed for the classroom
    total_owed = total_expenses - total_paid

    # Get the search query from the request
    search_query = request.GET.get('search')

    # Filter students based on the search query
    if search_query:
        students = classroom.student_set.filter(Q(name__icontains=search_query) | Q(national_number__icontains=search_query))
    else:
        students = classroom.student_set.all()

    # Paginate the students
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'classroom': classroom,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_expenses': total_expenses,
        'total_owed': total_owed,
        'total_paid': total_paid,
    }

    return render(request, 'students/classroom_details.html', context)





def g_reports(request):
    # Implement your view logic here
    return render(request, 'students/g_reports.html')


def generate_daily_report(request):
    report_date = date.today()
    start_date = report_date - timedelta(days=30)  # Change the number of days as needed
    
    daily_payments = Tuition.objects.filter(paid=True, receipt_date__date__range=[start_date, report_date]).values('receipt_date__date').annotate(total_amount=Sum('amount_tuition')).order_by('-receipt_date__date')

    paginator = Paginator(daily_payments, 10)  # Show 10 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'report_date': report_date,
        'daily_payments': page_obj
    }
    return render(request, 'students/daily_report.html', context)


def generate_student_report(request):
    # Retrieve all students
    students = Student.objects.all()

    context = {
        'report_data': students
    }

    return render(request, 'students/generate_student_report.html', context)

def generate_installment_report(request):
    # Retrieve all installments
    installments = Tuition.objects.all()

    context = {
        'installments': installments
    }
    return render(request, 'students/generate_installment_report.html', context)

def upgrade_students():
    # Retrieve all students who need to be upgraded
    students_to_upgrade = Student.objects.exclude(classroom__stage='Sec3')  # Exclude students already in the final stage

    # Define the upgrade rules
    upgrade_rules = {
        'BC': 'KG1',
        'KG1': 'KG2',
        'KG2': 'Prim1',
        'Prim1': 'Prim2',
        'Prim2': 'Prim3',
        'Prim3': 'Prim4',
        'Prim4': 'Prim5',
        'Prim5': 'Prim6',
        'Prim6': 'Prep7',
        'Prep7': 'Prep8',
        'Prep8': 'Prep9',
        'Prep9': 'Sec1',
        'Sec1': 'Sec2',
        'Sec2': 'Sec3',
    }

    # Loop through the students and upgrade them to the next educational stage
    for student in students_to_upgrade:
        current_stage = student.classroom.stage
        next_stage = upgrade_rules.get(current_stage)

        if next_stage:
            student.classroom = Classroom.objects.get(stage=next_stage)
        else:
            # If the student has reached the final stage, move them to the archive
            ArchiveStudent.objects.create(
                name=student.name,
                national_number=student.national_number,
                age=student.age,
                gender=student.gender,
                date_of_birth=student.date_of_birth,
                academic_year=student.academic_year,
                classroom=student.classroom.stage,
            )
            student.delete()  # Remove the student from the Student model

        # Save the changes to the student's classroom
        student.save()


def upgrade_students_view(request):
    if request.method == 'POST':
        # Perform the student upgrade process
        upgrade_students()

        # Set the success message
        success_message = "Students have been upgraded successfully."

        # Render the template with the success message
        return render(request, 'students/upgrade_students.html', {'success_message': success_message})

    # If it's a GET request, simply render the template without any message
    return render(request, 'students/upgrade_students.html')
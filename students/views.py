from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Sum
from django.core.paginator import Paginator
# from .models import EducationalStage, Expense
from django.db.models import Q
# Create your views here.

# def home(request):
#     return render(request, '/students/home.html')

from django.core.paginator import Paginator

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
    students = Student.objects.all()

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


@login_required
def register(request):
    if request.method == 'POST':
        academic_year_form = AcademicYearForm(request.POST)
        educational_stage_form = EducationalStageForm(request.POST)
        classroom_form = ClassroomForm(request.POST)
        if academic_year_form.is_valid() and educational_stage_form.is_valid() and classroom_form.is_valid():
            academic_year = academic_year_form.save()
            educational_stage = educational_stage_form.save()
            classroom = classroom_form.save(commit=False)
            classroom.educational_stage = educational_stage
            classroom.academic_year = academic_year
            classroom.save()
            messages.success(request, 'Registration successful!')
            return redirect('register')
    else:
        academic_year_form = AcademicYearForm()
        educational_stage_form = EducationalStageForm()
        classroom_form = ClassroomForm()
    context = {
        'academic_year_form': academic_year_form,
        'educational_stage_form': educational_stage_form,
        'classroom_form': classroom_form,
    }
    return render(request, 'students/register.html', context)

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


@login_required
def add_expense(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.student = student
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('add_expense', pk=pk)
    else:
        expense_form = ExpenseForm()
    context = {
        'student': student,
        'expense_form': expense_form,
    }
    return render(request, 'students/add_expense.html', context) 



# @login_required
# def pay_installment(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     student_name = student.name  # Retrieve the student's name
#     national_number = student.national_number  # Retrieve the student's national number

#     if request.method == 'POST':
#         installment_form = TuitionForm(request.POST)
#         if installment_form.is_valid():
#             installment = installment_form.save(commit=False)
#             installment.student = student
#             installment.paid = True  # Mark the installment as paid
#             installment.save()
#             messages.success(request, 'Installment paid successfully!')
#             return redirect('students:pay_installment', pk=pk)
#     else:
#         installment_form = TuitionForm()
    
#     context = {
#         'student': student,
#         'student_name': student_name,  # Pass the student's name to the template
#         'national_number': national_number,  # Pass the student's national number to the template
#         'installment_form': installment_form,
#     }
#     return render(request, 'students/pay_installment.html', context)

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
            return redirect('students:pay_installment', pk=pk)
    else:
        installment_form = TuitionForm()

    context = {
        'student': student,
        'student_name': student_name,
        'national_number': national_number,
        'installment_form': installment_form,
    }
    return render(request, 'students/pay_installment.html', context)

# @login_required
# def pay_installment(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     student_name = student.name  # Retrieve the student's name
#     national_number = student.national_number  # Retrieve the student's national number

#     if request.method == 'POST':
#         installment_form = TuitionForm(request.POST)
#         if installment_form.is_valid():
#             installment = installment_form.save(commit=False)
#             installment.student = student
#             installment.paid = True  # Mark the installment as paid
#             installment.payer = request.user.get_full_name()  # Set the payer's name automatically
#             installment.save()
#             messages.success(request, 'Installment paid successfully!')
#             return redirect('students:pay_installment', pk=pk)
#     else:
#         installment_form = TuitionForm()
    
#     context = {
#         'student': student,
#         'student_name': student_name,  # Pass the student's name to the template
#         'national_number': national_number,  # Pass the student's national number to the template
#         'installment_form': installment_form,
#     }
#     return render(request, 'students/pay_installment.html', context)

@login_required
def receipt(request, pk):
    tuition = get_object_or_404(Tuition, pk=pk)
    if not tuition.paid:
        messages.warning(request, 'This installment has not been paid yet.')
        return redirect('student_detail', pk=tuition.student.pk)
    else:
        context = {'tuition': tuition}
        return render(request, 'students/receipt.html', context)


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    installments = Tuition.objects.filter(student=student)
    total_paid = sum(installment.amount for installment in installments if installment.paid)
    context = {
        'student': student, 
        'installments': installments, 
        'total_paid': total_paid}
    return render(request, 'students/student_detail.html', context)

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class PayInstallmentView(LoginRequiredMixin, CreateView):
    model = Tuition
    form_class = TuitionForm
    template_name = 'students/pay_installment.html'
    success_url = reverse_lazy('students:student_detail')

    def form_valid(self, form):
        form.instance.student = self.get_student()
        form.instance.payer = self.request.user  # Set the payer to the current user
        return super().form_valid(form)


from django.db.models import Count, Sum

def report(request):
    # Number of registered students
    registered_students = Student.objects.count()

    # Total installments that have been paid
    total_paid_installments = Tuition.objects.filter(paid=True).count()

    # The total number of students who did not pay
    # total_unpaid_students = Student.objects.filter(tuition__paid=False).distinct().count()
    total_unpaid_students = Student.objects.filter(installments__paid=False).distinct().count()


    # Total male students
    total_male_students = Student.objects.filter(gender='M').count()

    # Total female students
    total_female_students = Student.objects.filter(gender='F').count()

    # Show statistics for all data on the application
    total_tuition = Tuition.objects.aggregate(total=Sum('amount'))['total']
    context = {
        'registered_students': registered_students,
        'total_paid_installments': total_paid_installments,
        'total_unpaid_students': total_unpaid_students,
        'total_male_students': total_male_students,
        'total_female_students': total_female_students,
        # 'stages': stages,
        'total_tuition': total_tuition,
    }
    return render(request, 'students/report.html', context)



def all_reports(request):
    # Number of registered students
    total_students = Student.objects.all().count()

    # Total installments that have been paid
    total_paid_tuitions = Tuition.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

    # The total number of students who did not pay
    total_unpaid_students = Student.objects.exclude(tuition__paid=True).count()

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
        unpaid_stage_students = stage_students.exclude(tuition__paid=True).count()
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
    total_paid_students = Student.objects.filter(tuition__paid=True).count()
    total_unpaid_tuitions = Tuition.objects.filter(paid=False).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_students': total_students,
        'total_paid_tuitions': total_paid_tuitions,
        'total_unpaid_students': total_unpaid_students,
        'total_male_students': total_male_students,
        'total_female_students': total_female_students,
        'stage_stats': stage_stats,
        'total_tuitions': total_tuitions,
        'total_paid_students': total_paid_students,
        'total_unpaid_tuitions': total_unpaid_tuitions,
    }

    return render(request, 'students/all_reports.html', context)

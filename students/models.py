from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class AcademicYear(models.Model):
    year = models.CharField(max_length=9)

    def __str__(self):
            return self.year

class EducationalStage(models.Model):
    name = models.CharField(max_length=50, verbose_name="Educational Stage")

    def __str__(self):
            return self.name
    
class Classroom(models.Model):
    STAGE_CHOICES = (
        ('1', 'Primary Stage'),
        ('2', 'Prep Stage'),
        ('3', 'Secondary Stage'),
        # add more stages as needed
    )
    stage = models.CharField(max_length=1, choices=STAGE_CHOICES, default='default_value', null=True)
    name = models.CharField(max_length=50, verbose_name="Class room")
    educational_stage = models.ForeignKey(EducationalStage, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    

    def __str__(self):
            return self.name
    
    
class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=50)
    national_number = models.IntegerField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    classroom = models.ManyToManyField(Classroom)
    
    def __str__(self):
            return self.name
    
class Expense(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
            return self.student
    # Chat GPT try
class Tuition(models.Model):
    student = models.ForeignKey(Student, related_name='installments', on_delete=models.CASCADE)
    installment_number = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    receipt_date = models.DateField(default=now)


    def __str__(self):
            return f"Installment #{self.installment_number} for {self.student.name}"
    # end chat GPT


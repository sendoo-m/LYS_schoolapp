from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class AcademicYear(models.Model):
    STAGE_CHOICES = (
        ('1', '2021-2022'),
        ('2', '2022-2023'),
        ('3', '2023-2024'),
    )
    year = models.CharField(max_length=50, choices=STAGE_CHOICES, verbose_name="Academic Year", default='default_value', null=True)

    def __str__(self):
            return self.year

class EducationalStage(models.Model):
    STAGE_CHOICES = (
        ('1', 'Primary Stage'),
        ('2', 'Prep Stage'),
        ('3', 'Secondary Stage'),
    )

    name = models.CharField(max_length=50, choices=STAGE_CHOICES, verbose_name="Educational Stage", default='default_value', null=True)

    def __str__(self):
            return self.name
    
class Classroom(models.Model):
    CLASS_CHOICES = (
        ('', 'اختار المرحلة التعليمية'),
        ('BC', 'مرحلة تمهيدي'),
        ('KG1', 'رياض أطفال 1'),
        ('KG2', 'رياض أطفال 2'),
        ('Prim1', 'الصف الأول الابتدائي- Grade 1'),
        ('Prim2', 'الصف الثاني الابتدائي- Grade 2'),
        ('Prim3', 'الصف الثالث الابتدائي- Grade 3'),
        ('Prim4', 'الصف الرابع الابتدائي- Grade 4'),
        ('Prim5', 'الصف الخامس الابتدائي- Grade 5'),
        ('Prim6', 'الصف السادس الابتدائي- Grade 6'),
        ('Prep7', 'الصف الأول الإعدادي- Grade 7'),
        ('Prep8', 'الصف الثاني الإعدادي- Grade 8'),
        ('Prep9', 'الصف الثالث الإعدادي- Grade 9'),
        ('Sec1', 'الصف الأول الثانويSecondary School 1'),
        ('Sec2', 'الصف الثاني الثانويSecondary School 2'),
        ('Sec3', 'الصف الثالث الثانويSecondary School 3'),
        
    ) 
        # add more stages as needed
    stage = models.CharField(max_length=1, choices=CLASS_CHOICES, default='default_value', null=True)
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
    student = models.ForeignKey(Student, related_name='student_Expense', on_delete=models.CASCADE)
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

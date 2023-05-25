from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


# Create your models here.

class EducationalStage(models.Model):
    STAGE_CHOICES = (
        ('', 'اختار المرحلة الدراسية'),
        ('BC', 'babyclass'),
        ('Kindergarten', 'Kindergarten'),
        ('Primary Stage', 'Primary Stage'),
        ('Prep Stage', 'Prep Stage'),
        ('Secondary Stage', 'Secondary Stage'),
    )

    name = models.CharField(max_length=50, choices=STAGE_CHOICES, verbose_name="Educational Stage", default='default_value', null=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    CLASS_CHOICES = (
        ('', 'اختار الصف الدراسي'),
        ('BC', 'babyclass'),
        ('KG1', 'Kindergarten 1'),
        ('KG2', 'Kindergarten 2'),
        ('Prim1', 'Grade 1'),
        ('Prim2', 'Grade 2'),
        ('Prim3', 'Grade 3'),
        ('Prim4', 'Grade 4'),
        ('Prim5', 'Grade 5'),
        ('Prim6', 'Grade 6'),
        ('Prep7', 'Grade 7'),
        ('Prep8', 'Grade 8'),
        ('Prep9', 'Grade 9'),
        ('Sec1', 'Secondary School 1'),
        ('Sec2', 'Secondary School 2'),
        ('Sec3', 'Secondary School 3'),
    )

    name = models.CharField(max_length=100, default='Default Classroom Name', null=True)
    stage = models.CharField(max_length=50, choices=CLASS_CHOICES, default='default_value', null=True)
    educational_stage = models.ForeignKey(EducationalStage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class AcademicYear(models.Model):
    year = models.CharField(max_length=4, unique=True, default='2023')

    def __str__(self):
        return self.year


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
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, default=timezone.now)
    classroom = models.ManyToManyField(Classroom)

    def __str__(self):
        return self.name

 

from django.db.models import F

class Expense(models.Model):
    classroom = models.ForeignKey(Classroom, related_name='classroom_expenses', on_delete=models.CASCADE, null=True)
    expense_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return str(self.expense_type)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        
    # end chat GPT
class Tuition(models.Model):
    student = models.ForeignKey(Student, related_name='installments', on_delete=models.CASCADE)
    # classroom = models.ForeignKey(Classroom, related_name='tuition', on_delete=models.CASCADE, null=True) # زيادة للتجربه
    installment_number = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    receipt_date = models.DateField(default=now)

    def __str__(self):
        return f"Installment #{self.installment_number} for {self.student.name}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.timestamp}"

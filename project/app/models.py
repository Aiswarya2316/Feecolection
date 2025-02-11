from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=150)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    



class FeeDetail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def due_amount(self):
        return self.total_fee - self.paid_amount

    def __str__(self):
        return f"Fees for {self.student.user.username}"



class FeeStructure(models.Model):
    course = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, unique=True)

from django import forms
from django.contrib.auth.models import User
from .models import Student, Owner

class StudentRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['course', 'contact']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        student = Student(user=user, course=self.cleaned_data['course'], contact=self.cleaned_data['contact'])
        if commit:
            user.save()
            student.save()
        return student

class OwnerRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Owner
        fields = ['business_name', 'contact']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        owner = Owner(user=user, business_name=self.cleaned_data['business_name'], contact=self.cleaned_data['contact'])
        if commit:
            user.save()
            owner.save()
        return owner


from django import forms
from .models import FeeDetail

class FeeDetailForm(forms.ModelForm):
    class Meta:
        model = FeeDetail
        fields = ['student', 'total_fee', 'paid_amount']

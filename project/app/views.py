from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentRegisterForm, OwnerRegisterForm

def register_student(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            student = form.save()
            login(request, student.user)  # Auto-login after registration
            return redirect("login_student")
    else:
        form = StudentRegisterForm()
    return render(request, "student/registerstd.html", {"form": form})

def register_owner(request):
    if request.method == "POST":
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            owner = form.save()
            login(request, owner.user)  # Auto-login after registration
            return redirect("login_owner")
    else:
        form = OwnerRegisterForm()
    return render(request, "owner/registerowner.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student, Owner
from django.contrib.auth.forms import AuthenticationForm

def login_student(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                # Check if user is a student
                if Student.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect("homestudent")
                else:
                    messages.error(request, "You are not registered as a student!")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "student/loginstd.html", {"form": form})

def login_owner(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                # Check if user is an owner
                if Owner.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect("homeowner")
                else:
                    messages.error(request, "You are not registered as an owner!")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "owner/loginowner.html", {"form": form})


from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_student(request):
    logout(request)
    return redirect("home")  # Redirect to student login page

def logout_owner(request):
    logout(request)
    return redirect("home")  # Redirect to owner login page


def home(request):
    return render(request,'home.html')


def homestudent(request):
    return render(request,'student/homestudent.html')


def homeowner(request):
    return render(request,'owner/homeowner.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FeeDetail, Student
from .forms import FeeDetailForm

def add_fee_details_of_student(request):
    if request.method == "POST":
        form = FeeDetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee details added successfully!")
            return redirect("view_fee_details_of_student")
    else:
        form = FeeDetailForm()
    
    return render(request, "owner/feedetails.html", {"form": form})

def view_fee_details_of_student(request):
    fee_details = FeeDetail.objects.all()
    return render(request, "owner/viewdetails.html", {"fee_details": fee_details})



import razorpay
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FeeDetail, Student

@login_required
def detailsoffees(request):
    try:
        student = Student.objects.get(user=request.user)
        student_fees = FeeDetail.objects.filter(student=student).first()
    except Student.DoesNotExist:
        student_fees = None

    context = {
        'total_fee': student_fees.total_fee if student_fees else 0,
        'paid_amount': student_fees.paid_amount if student_fees else 0,
        'due_amount': (student_fees.total_fee - student_fees.paid_amount) if student_fees else 0
    }
    
    return render(request, 'student/detailsoffees.html', context)

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import FeeDetail, Student, Payment

@login_required
def payment(request):
    try:
        student = Student.objects.get(user=request.user)
        student_fees = FeeDetail.objects.filter(student=student).first()
        due_amount = (student_fees.total_fee - student_fees.paid_amount) if student_fees else 0
    except Student.DoesNotExist:
        due_amount = 0

    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create a Razorpay order
    payment_order = razorpay_client.order.create({
        "amount": int(due_amount * 100),  # Amount in paise (₹1 = 100 paise)
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "amount": due_amount,
        "razorpay_order_id": payment_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "currency": "INR"
    }
    return render(request, 'student/payment.html', context)


import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        razorpay_order_id = data.get("razorpay_order_id")
        payment_id = data.get("razorpay_payment_id")
        signature = data.get("razorpay_signature")

        try:
            # Verify payment signature
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                # Get student details
                student = Student.objects.get(user=request.user)
                student_fees = FeeDetail.objects.filter(student=student).first()

                # Store Payment Record in Database
                Payment.objects.create(
                    student=student,
                    amount_paid=student_fees.total_fee - student_fees.paid_amount,
                    transaction_id=payment_id
                )

                # Update Fee Details
                student_fees.paid_amount = student_fees.total_fee  # Mark full amount as paid
                student_fees.save()

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Payment verification failed."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def payment_success(request):
    return render(request, "student/payment_success.html")


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/profile.html', {'student': student})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def studentprofile(request):
    students = Student.objects.all()
    return render(request, 'owner/studentprofile.html', {'students': students})


from django.shortcuts import render, redirect
from .models import FeeStructure
from django.contrib import messages
from datetime import datetime

def addfeestructure(request):
    if request.method == "POST":
        course = request.POST.get("course")
        yearly_amount = request.POST.get("yearly_amount")
        year = request.POST.get("year")

        if course and yearly_amount and year:
            FeeStructure.objects.create(
                course=course,
                yearly_amount=yearly_amount,
                year=year
            )
            messages.success(request, "Fee structure added successfully!")
            return redirect("viewfeestructure")

    return render(request, "owner/addfeestructure.html")



from django.shortcuts import render
from .models import FeeStructure
from datetime import datetime

def viewfeestructure(request):
    fees = FeeStructure.objects.all()
    return render(request, "owner/viewfeestructure.html",{'fees':fees})

def viewstructure(request):
    fees = FeeStructure.objects.all()
    return render(request, "student/viewfeestructure.html",{'fees':fees})
















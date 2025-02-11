from django.urls import path
from .views import register_student, register_owner, login_student, login_owner,homestudent,homeowner,logout_owner,logout_student,add_fee_details_of_student, view_fee_details_of_student,detailsoffees,home,payment,payment_success,verify_payment,student_profile

urlpatterns = [
    path('',home,name="home"),
    path("registerstudent/", register_student, name="register_student"),
    path("registerowner/", register_owner, name="register_owner"),
    path("loginstudent/", login_student, name="login_student"),
    path("loginowner/", login_owner, name="login_owner"),
    path("homestudent/", homestudent, name="homestudent"),
    path("homeowner/", homeowner, name="homeowner"),
    path("logoutstudent/", logout_student, name="logout_student"),
    path("logoutowner/", logout_owner, name="logout_owner"),
    path("addfeedetailsofstudent/", add_fee_details_of_student, name="add_fee_details_of_student"),
    path("viewfeedetailsofstudent/", view_fee_details_of_student, name="view_fee_details_of_student"),
    path("detailsoffees/", detailsoffees, name="detailsoffees"),
    path('payment/', payment, name='payment'),
    path('payment-success/', payment_success, name='payment_success'),
    path("verify-payment/", verify_payment, name="verify_payment"),
    path("student/<int:student_id>/", student_profile, name="student_profile"),




]

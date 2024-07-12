"""mrds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.messages import success
from django.urls import path
from web_app import views as web_views
from refer_app import views as refer_views
from admin_app import views as admin_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('siteadmin', admin.site.urls),
    path("", web_views.homeView, name="home"),
    path("index", web_views.homeView, name="home"),
    path("login", web_views.loginView, name="login"),
    path("login/<str:user_type>", web_views.loginView, name="login"),
    path('logout', web_views.logout, name='logout'),
    path("register", web_views.registerView, name="register"),
    path("register/<str:user_type>", web_views.registerView, name="register"),
    path("register/<str:user_type>/<str:referral_code>", web_views.registerView, name="register"),
    path("profile", web_views.profile_view, name="profile"),
    path("profile/edit", web_views.profileEditView, name="profileEdit"),
    path("search", web_views.searchView, name="search"),
    path("cart", web_views.cartView, name="cart"),
    path("common-page", web_views.commonpageView, name="commonpage"),
    path("ajax/registeruser", web_views.registerUser, name="registerUser"),
    path("ajax/loginuser", web_views.loginUser, name="loginUser"),
    path("ajax/updateuser", web_views.updateUser, name="updateUser"),
    path("profile_upload",web_views.profile_image_view , name = 'image_upload'),
    path("image_upload",web_views.upload_image_view , name = 'upload_image_view'),
    path('success', web_views.success, name = 'success'),
    path('appointment', web_views.appointment, name = 'appointment'),
    path('cancellation-policy',web_views.cancellationpolicyView,name="cancellationpolicy"),
    path('consent',web_views.consentView,name="consent"),
    path('moupt',web_views.mouptView,name="moupt"),
    path('terms-condition',web_views.termsconditionView,name="termscondition"),
    path('thank-you/<str:order_id>', web_views.thankyouView, name="thankyou"),
    path('privacy-policy',web_views.privacypolicyView,name="privacypolicy"),
    path('ajax/show_appointment_slots', web_views.showAppointmentAjax, name="showAppointmentAjax"),
    path("payment",web_views.paymentView,name="payment"),
    path("checkstatus",web_views.checkStatusView,name="checkStatus"),
    path("ajax/appointmentSave",web_views.appointmentSave,name="checkStatus"),
    path("ajax/paymentSave",web_views.paymentSave,name="checkStatus"),
    path("my-appointments",web_views.myAppointmentView,name="checkStatus"),
    path("my-patients",web_views.patientAppointmentView,name="checkStatus"),
    path("ajax/update-appointment",web_views.updateAppointmentAjax,name="checkStatus"),
    path("ajax/search-dr",web_views.searchDrAjax,name="searchDrAjax"),
    path("referred-patients",web_views.patientReferView,name="searchDrAjax"),
    path("referred-doctors",web_views.doctorReferView,name="searchDrAjax"),
    path('doctor/profile/<int:dr_id>', web_views.doctorProfileView, name="doctorProfile"),
    path('refer/login', refer_views.loginView, name="referLogin"),
    path('refer/ajax/login', refer_views.ajaxLogin, name="referpatient"),
    path('refer/ajax/patient', refer_views.ajaxRefer, name="referpatient"),
    path('refer/dashboard', refer_views.dashboardView, name="referDashboard"),
    path('refer', refer_views.dashboardView, name="referDashboard"),
    path('refer/patient', refer_views.referView, name="referpatient"),
    path('refer/logout', refer_views.logout, name="referpatient"),
    path('admin/login', admin_views.loginView, name="referLogin"),
    path('admin/register', admin_views.registerView, name="referHome"),
    path('admin', admin_views.dashboardView, name="referDashboard"),
    path('admin/dashboard', admin_views.dashboardView, name="referDashboard"),
    path('admin/logout', admin_views.logout, name="referpatient"),
    path('admin/ajax/login', admin_views.ajaxLogin, name="referpatient"),
    path('admin/doctor', admin_views.doctordView, name="referpatient"),
    path('admin/pt', admin_views.ptView, name="referpatient"),
    path('admin/patient', admin_views.patientView, name="referpatient"),
    path('admin/ajax/register', admin_views.ajaxRegister, name="referpatient"),
    path('admin/referrals', admin_views.referralView, name="referpatient"),
    path('admin/coupons', admin_views.couponsView, name="couponsView"),
    path('admin/ajax/add-coupon', admin_views.ajaxAddCoupon, name="addcoupon"),
    path('admin/ajax/update-coupon', admin_views.ajaxUpdateCoupon, name="deactivatecoupon"),
    path('ajax/apply-coupon', web_views.applyCouponAjax, name="applyCouponAjax"),
    path('ajax/rzp', web_views.getPaymentAjax, name="applyCouponAjax"),
    path('subscription', web_views.subscriptionView, name="subscription"),
    path('ajax/patient/get', refer_views.getPatientView, name="getPatient"),
    path('reset-password', web_views.resetPasswordView, name="resetpassword"),
    path('forgot-password', web_views.forgotPasswordView, name="forgotpassword"),
    path('validate-otp', web_views.validate_otp, name='validate_otp'),
    path('reset-password', web_views.resetPasswordView, name='reset_password_confirm')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

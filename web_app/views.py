
from django.shortcuts import render
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import redirect
from services.UserService import UserService
from services.OtpService import OtpService
from services.EmailService import EmailService
from services.UtilService import *
from datetime import date
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
import json
import datetime as dt
import requests
from django.template.loader import render_to_string
from services.ReferService import ReferService
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from services.CouponService import CouponService
#from web_app.models import Refer


User = UserService()
Refer = ReferService()
Coupon = CouponService()


def loggedin(fun):
    def inner(request, *args, **kwargs):
        if 'loggedin_user' not in request.session:
            return redirect('/login')
        else:
            return fun(request, *args, **kwargs)
    return inner


def logout(request):
    try:
        del request.session['loggedin_user']
    except:
        return redirect('/login')
    return redirect('/login')

# Create your views here.

def homeView(request):
    user_data = request.session.get('loggedin_user', {})
    return render(request,"web_app/home.html", {'user_data':user_data})


def validate_input(username, password):
    if not username or not password:
        return False
    return True

def loginView(request,user_type=None):
    if 'loggedin_user' in request.session:
        del request.session['loggedin_user']

    user_type_id = 1
    if user_type=='dr':
        user_type_id = 2
    return render(request,"web_app/login.html", {'user_type_id':user_type_id})

@csrf_exempt
def searchView(request):
    user_data = request.session.get('loggedin_user', {})
    print(user_data)
    search_keyword = request.POST.get('search_keyword', '')
    search_city = request.POST.get('search_city', '')
    print(search_keyword)
    result = User.search_user(search_keyword, search_city)
    print(result)
    return render(request,"web_app/search-page.html", {'data':{'keyword':search_keyword, 'city':search_city},'result': result,'user_data':user_data})
    #return render(request, "web_app/search-page.html",{})

@csrf_exempt
def searchDrAjax(request):
    user_data = request.session.get('loggedin_user', {})
    print(user_data)
    search_keyword = request.POST.get('search_keyword')
    search_city = request.POST.get('search_city')
    print(search_keyword)
    result = User.search_user(search_keyword, search_city, user_data['id'])
    print(result)
    search_data = render_to_string("web_app/search-ajax.html", {'data':{'keyword':search_keyword, 'city':search_city},'result': result,'user_data':user_data})
    return JsonResponse({'search_data': search_data, 'status': 'success'})


@csrf_exempt
@loggedin
def cartView(request):
    user_data = request.session.get('loggedin_user', {})
    apt_data = request.POST
    print(apt_data)
    apt_arr = apt_data.get('user_apt_data').split("_")
    user_id = apt_arr[0]
    apt_date = apt_arr[2]
    apt_time = apt_arr[3]
    user_info = User.get_user_all_info(user_id)
    user_info.gst_amount = int(user_info.consultation_fees) * 0.18
    user_info.total_amount = int(user_info.consultation_fees) + user_info.gst_amount
    request.session['cart'] = {'user_id': user_id, 'amount':user_info.consultation_fees, 'final_amount':user_info.total_amount, 'apt_date':apt_date, 'apt_time':apt_time, 'doctor_id': user_id,}
    print(user_info )
    return render(request,"web_app/cart.html",{'user_info': user_info, 'apt_date':apt_date, 'apt_time':apt_time,'user_data':user_data})

def commonpageView(request):
    return render(request,"web_app/common-page.html",{})

def is_valid_user_input(username, email, password):
    # Implement your validation logic here
    # For example, check if fields are not empty and meet specific criteria
    if not username or not email or not password:
        return False
    # Add more validation rules as needed (e.g., check email format, password strength, etc.)
    return True


def registerView(request,user_type=None, referral_code=None):
    print(user_type)
    print(referral_code)
    user_type_id = 1
    data = object()
    if referral_code is not None:
        data = Refer.get_refer({'referral_code':referral_code})

    return render(request,"web_app/register.html", {'data': data, 'user_type': user_type_id})

def cancellationpolicyView(request):
    return render(request,"web_app/cancellationpolicy.html")

def consentView(request):
    return render(request,"web_app/consent.html")

def mouptView(request):
    return render(request,"web_app/moupt.html")

def termsconditionView(request):
    return render(request,"web_app/termscondition.html")

def privacypolicyView(request):
    return render(request,"web_app/privacypolicy.html")

def subscriptionView(request):
    return render(request,"web_app/subscription.html")


@loggedin
def thankyouView(request, order_id):
    loggedin_user_data = request.session.get('loggedin_user', {})
    return render(request,"web_app/thank-you.html", {'order_id':order_id, 'user_data':loggedin_user_data})

@csrf_exempt
@loggedin
def paymentView(request):
    loggedin_user_data = request.session.get('loggedin_user', {})
    # Making a POST request
    session_cart = request.session.get('cart', {})
    print(session_cart)
    if not session_cart:
        return redirect('/cart')
    amount  =   session_cart['final_amount']
    amount_in_paise = session_cart['final_amount']*100
    url = "https://sandbox.cashfree.com/pg/orders"

    where_user = {'user_id': loggedin_user_data['id'], "is_active": 1}
    user = User.get_user(where_user)
    user_id = str(user.user_id)
    user_name = user.user_first_name + " " + user.user_last_name
    user_email = user.user_email
    user_phone = user.user_mobile
    data = {"customer_details": {"customer_id": user_id, "customer_email": user_email, "customer_phone": "1299087801"},
            "order_amount": amount, "order_currency": "INR", "order_note": user_name}
    print(data)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-version": "2022-09-01",
        "x-client-id": "300878ec5183cd4fc116774a73878003",
        "x-client-secret": "2f7ff2e913fc59714e6f2c7d77ba4114fedc2e01"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    # check status code for response received
    # success code - 200
    print(r)
    # print content of request
    resp = r.json()
    print(resp['payment_session_id'])
    return render(request,"web_app/payment.html", {'pay_data':resp['payment_session_id'], 'user': user,'payment_amount':amount,'payment_amount_in_paise':amount_in_paise, 'user_data':loggedin_user_data} )

@csrf_exempt
def checkStatusView(request):
    req = request.POST
    orderId=req.get('order_id')
    url = "https://sandbox.cashfree.com/pg/orders/" + orderId

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-version": "2022-09-01",
        "x-client-id": "300878ec5183cd4fc116774a73878003",
        "x-client-secret": "2f7ff2e913fc59714e6f2c7d77ba4114fedc2e01"
    }
    r = requests.get(url, headers=headers)
    resp = r.json()
    print("status")
    print(resp['order_status'])
    return JsonResponse({'order_status': resp['order_status'], 'status': 'success'})

@loggedin
def doctorProfileView(request, dr_id):
    user_data = request.session.get('loggedin_user', {})
    data = User.get_user_all_info(dr_id)
    print(data.profile_image_name)
    ca_header, ca_slot = getAppointmentSlots(dr_id)
    profile_template = "web_app/profile-dr.html"

    return render(request, profile_template, {'user_data':user_data, 'data' : data, 'clinicAvailibility': {
        'header':ca_header, 'time_slot':ca_slot}})


@loggedin
def profileView(request):
    user_data = request.session.get('loggedin_user', {})
    data = User.get_user_all_info(user_data['id'])
    ca_header, ca_slot = {}, {}
    profile_template = "web_app/profile-dr-internal.html"
    if user_data['user_type'] == 1:
        profile_template = "web_app/profile-patient.html"
    else:
        ca_header, ca_slot = getAppointmentSlots(user_data['id'])


    return render(request, profile_template, {'user_data':user_data, 'data' : data, 'clinicAvailibility': {
        'header':ca_header, 'time_slot':ca_slot}})

@csrf_exempt
def showAppointmentAjax(request):
    req = request.POST
    user_id = req.get('user_id')
    ca_header, ca_slot = getAppointmentSlots(user_id)
    #return render(request,"web_app/slot-calender.html", {'clinicAvailibility': {'header':ca_header, 'time_slot':ca_slot}})

    html = render_to_string("web_app/slot-calender.html", {'clinicAvailibility': {
        'header':ca_header, 'time_slot':ca_slot, 'user_id':user_id}})
    return JsonResponse(html, safe=False)

@csrf_exempt
@loggedin
def profileEditView(request):
    user_data = request.session.get('loggedin_user', {})
    print(user_data)
    if request.method == 'POST':
        print("I am here 1")
        #form =ProfileImageForm(request.POST, request.FILES)
        print(request.FILES)

        f = request.FILES['profile_Main_Img']
        print(f)
        #uploaded_path = 'templates/static/profiles/'
        uploaded_path = settings.MEDIA_ROOT + '/profiles/'
        print(uploaded_path)
        uploaded_file_name = str(request.session['loggedin_user']['id'])+ '.' +f.name.split('.')[1]


        with open( uploaded_path+uploaded_file_name , 'wb+') as destination:

            for chunk in f.chunks():
                destination.write(chunk)

        user_image = {}
        user_image['profile_image_name'] = uploaded_file_name
        where = {'user_id': request.session['loggedin_user']['id']}
        User.update_user(user_image, where)


    where_user = {'user_id': user_data['id'], "is_active": 1}
    where_user_type = where = {'user_type_id': user_data['user_type'], "is_active": 1}

    subscription = User.get_subscription(where_user_type, field=['subscription_id', 'subscription_name', 'cost'])
    user = User.get_user(where_user)


    address = User.get_user_address({'user_id': user_data['id']})
    user_subscription = User.get_user_subscription(where=where_user,
                                                   field=['subscription_id'])
    user_subscription = [i.subscription_id for i in user_subscription] if user_subscription else []
    specialization = {}
    qualification = {}
    user_specialization = {}
    user_qualification = {}
    profile = {}
    profile = User.get_user_profile({'user_id': user_data['id']})
    if user_data['user_type'] in [2, 3, '2', '3']:

        specialization = User.get_specialization(where_user_type, field=['specialization_id', 'specialization'])
        qualification = User.get_qualification(where_user_type, field=['qualification_id', 'qualification'])
        user_specialization = User.get_user_specialization(where=where_user,
                                                           field=['specialization_id'])
        user_qualification = User.get_user_qualification(where=where_user,
                                                         field=['qualification_id'])
        user_specialization = [i.specialization_id for i in user_specialization] if user_specialization else []
        user_qualification = [i.qualification_id for i in user_qualification] if user_qualification else []

    data = {'user': user, 'specialization': specialization, 'qualification': qualification,
            'subscription': subscription, 'profile': profile, 'address': address,
            'user_specialization': user_specialization, 'user_qualification': user_qualification,
            'user_subscription': user_subscription}

    days = ('monday', 'tuesday','wednesday','thursday','friday','saturday','sunday')
    duration = range(1, 61)
    return render(request, "web_app/profile-edit.html", {'user_data': user_data, 'data': data, 'days':days, 'duration':duration})
    # return render(request, "web_app/profile-page.html", {})

@csrf_exempt
@loggedin
def clinicAvailibilityView(request):
    user_data = request.session.get('loggedin_user', {})
    print(user_data)
    where_user = {'user_id': user_data['id'], "is_active": 1}
    where_user_type = where = {'user_type_id': user_data['user_type'], "is_active": 1}

    clinicAvailibility  = User_Clinic_Availibility(where_user_type, field=['User_Clinic_Availibility', 'day', 'start_time','end_time','duration','user_id','is_available'])
    print(clinicAvailibility)
    user = User.get_user(where_user)
    clinicAvailibility = {}

    if user_data['user_type'] in [2, 3, '2', '3']:

        clinicAvailibility = User.get_user_clinic_availibility(where=where_user,
                                                           field=['user_id'])
    data = {'user':user, 'user_clinic_availibity': clinicAvailibility}
    print(data)
    return render(request, "web_app/profile-page.html", {'user_data': user_data, 'data': data})
    # clinicAvailibity1 = User_Clinic_Availibility.Objects.all()
    # return render(request,"web_app/profile-page.html",{clinicAvailibity1})

@csrf_exempt
def registerUser(request):

    req = request.POST
    data = {}
    data['user_first_name'] = req.get('first_name')
    data['user_last_name'] = req.get('last_name')
    data['user_email'] = req.get('email_address')
    data['user_mobile'] = req.get('mobile_number')
    data['user_type_id'] = req.get('user_type')
    data['user_mobile'] = req.get('mobile_number')
    data['user_type_id'] = int(req.get('user_type'))
    data['password'] = req.get('password')
    data['user_name'] = req.get('email_address')
    data['referral_code'] = req.get('referral_code')
    if data['referral_code'].strip() != '':
        is_referred = Refer.get_refer(
            {'email': data['user_email'], 'referral_code': data['referral_code']})
        if not is_referred:
            return JsonResponse({'resp': 'Invalid referral code', 'status': 'failed'})
    user = User.get_user({'user_email':data['user_email'],'user_type_id':data['user_type_id'], 'is_active':1})
    if user:
        return JsonResponse({'resp': 'User already exist', 'status': 'failed'})

    # action = req.get('action')
    # if action == 'send_otp':
    #     otpObj = OtpService()
    #     otp = otpObj.generate()
    #     if otpObj.sendEmailOtp(data['user_email']):
    #         request.session['otp'] = str(otp)
    #         return JsonResponse({'resp': "OTP sent to "+data['user_email'], 'status': 'success'})
    #     else:
    #         return JsonResponse({'resp': "Error to send OTP", 'status': 'fail'})
    #
    # if action== 'validate_otp':
    #     received_otp = req.get('otp')
    #     #if received_otp != cache.get(data['user_mobile']):
    #     if received_otp != request.session['otp']:
    #         return JsonResponse({'resp': 'Invalid OTP', 'status': 'failed'})

    #    else:
    user_id = User.add_user(data)

    where_user = {'user_id': user_id, "is_active": 1}
    user_subscription = User.get_user_subscription(where=where_user,
                                                   field=['subscription_id'])
    userdata = {"id": user_id,
                "first_name": data['user_first_name'],
                "last_name": data['user_last_name'],
                "user_type": data['user_type_id']}
    if user_subscription:
        userdata['subscription'] = 1
    else:
        userdata['subscription'] = 0

    request.session['loggedin_user'] = userdata

    return JsonResponse({'resp': 'redirect', 'status': 'success'})


@csrf_exempt
def loginUser(request):
    print(request.POST)
    req = request.POST
    data = {}

    #perform server side validation on email
    email = req.get('email')

    data['user_name'] = req.get('email')
    data['password'] = req.get('password')
    data['user_type_id'] = req.get('user_type')

    user = User.get_user(data)
    if not user:
        return JsonResponse({'resp': 'User doesn\'t exist', 'status': 'failed'})

    userdata = {"id": user.user_id,
                "first_name": user.user_first_name,
                "last_name": user.user_last_name,
                "user_type": user.user_type_id}

    request.session['loggedin_user'] = userdata
    # return redirect('home')
    return JsonResponse({'resp': 'redirect', 'status': 'success'})

@csrf_exempt
@loggedin
def updateUser(request):
    data = request.POST
    action=data.get('action')
    where = {'user_id': request.session['loggedin_user']['id']}

    if action == 'update_personal_info':

        user={}

        user['user_first_name']=data.get('first_name')
        user['user_last_name']=data.get('last_name')
        user['gender']=data.get('gender')
        user['dob']=data.get('dob')
        user['user_email']=data.get('email')
        User.update_user(user,where)

    if action == 'update_profile_info':
        user_profile={}
        user_profile['about_me']=data.get('about_me')
        user_profile['total_experience']=data.get('total_experience')
        user_profile['consultation_fees']=data.get('consultation_fees')
        User.update_user_profile(user_profile,where)


    if action == 'update_address_info':

        user_address={}

        user_address['title']=data.get('title')
        user_address['address_1']=data.get('address_1')
        user_address['address_2']=data.get('address_2')
        user_address['city']=data.get('city')
        user_address['dist']=data.get('district')
        user_address['state']=data.get('state')
        user_address['pincode']=data.get('pincode')
        user_address['address_type']=1
        user_address['is_active']=1
        where={'user_id':request.session['loggedin_user']['id']}
        User.update_user_address(user_address,where)

    if action == 'update_professional_info':
        where = {'user_id': request.session['loggedin_user']['id']}
        User.delete_user_qualification(where)
        User.delete_user_specialization(where)
        qualification_list = data.get('qualification').split(',')
        for q_id in qualification_list:
            user_qualification={}
            user_qualification['qualification_id']=q_id
            user_qualification['user_id']=request.session['loggedin_user']['id']
            user_qualification['is_active'] = 1
            User.add_user_qualification(user_qualification)

        specialization_list = data.get('specialization').split(',')
        for s_id in specialization_list:
            user_specialization={}
            user_specialization['specialization_id']=s_id
            user_specialization['user_id'] = request.session['loggedin_user']['id']
            user_specialization['is_active'] = 1
            User.add_user_specialization(user_specialization)

    if action == 'update_subscription_info':

        today = date.today()

        user_subscription = {}
        user_subscription['subscription_id'] = data.get('subscription_id')
        user_subscription['user_id'] = request.session['loggedin_user']['id']
        where_s={"subscription_id": data.get('subscription_id'), "is_active": 1}
        subscription = User.get_subscription(where_s, field=['subscription_validity'])
        validity = int(subscription[0].subscription_validity)
        subscription_start = today.strftime("%Y-%m-%d 00:00:00")
        subscription_end = (today + relativedelta(months=validity)).strftime("%Y-%m-%d 00:00:00")

        user_subscription['subscription_start'] = subscription_start
        user_subscription['subscription_end'] = subscription_end
        user_subscription['is_active'] = 1
        where = {'user_id': request.session['loggedin_user']['id']}
        User.update_user_subscription(user_subscription, where)

    if action == 'update_availability_info':
        User_Clinic_Availibility ={}

        availDict = json.loads(data.get('avail'))
        typeAvail = type(availDict)
        for day, valStr in availDict.items():

            User_Clinic_Availibility['day']=day
            valList = valStr.split(",")
            User_Clinic_Availibility['start_time']=valList[0]
            User_Clinic_Availibility['end_time']=valList[1]
            User_Clinic_Availibility['duration']=valList[2]
            User_Clinic_Availibility['is_available']=valList[3]
            print(User_Clinic_Availibility)
            where = {'user_id': request.session['loggedin_user']['id'], 'day':day}
            User.update_user_clinic_availibiliy(User_Clinic_Availibility,where)
            print("-----------------------")
            print("mydata",data)

    return JsonResponse({'resp': data})

# Create your views here.

@loggedin
def profile_image_view(request):
    if request.method == 'POST':
        form =ProfileImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ProfileImageForm()
    return render(request, 'UploadPic.html', {'form': form})


# Create your views here.
def set_appintment_ajax(request):
    if request.method == 'POST':
        data = request.POST
        apt_date_list = data.get('apt_date').split("-")
        apt_date_ymd = apt_date_list[2]+"-"+apt_date_list[1]+"-"+apt_date_list[0]
        apt_time = data.get('apt_time')+":00"
        apt_user = data.get('apt_user')
        apt_data = {}
        apt_data['patient_id'] = request.session['loggedin_user']['id']
        apt_data['appointment_datetime'] = "{0} {1}".format(apt_date_ymd, apt_time)
        apt_data['user_clinic_id'] = 1
        apt_data['appointment_type'] = "at_clinic"
        apt_data['appointment_status'] = "open"
        apt_data['payment_type'] = ""

    return JsonResponse({'resp': data})

@csrf_exempt
def upload_image_view(request):
    if request.method == 'POST':
        print("I am here 1")
        #form =ProfileImageForm(request.POST, request.FILES)
        print(request.FILES)
        name = request.POST['profileName']
        print(name)
        uploaded_path = settings.MEDIA_ROOT + '/profiles/'
        print(uploaded_path)
        f = request.FILES['profile_Main_Img']
        print(f)
        #uploaded_path = 'web_app/static/profiles/'

        uploaded_file_name = str(request.session['loggedin_user']['id'])+ '.' +f.name.split('.')[1]

        with open( uploaded_path+uploaded_file_name , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    return render(request, 'web_app/profile-edit.html')

def upload_image_show(request):
    all_uploads = profile_image_view.objects.all()
    return render(request,'web_app/profile-page.html',{'uploads': all_uploads})

def success(request):
    return HttpResponse('successfully uploaded')

def appointment(request):
        return render(request,"web_app/appointment.html",{})

def getAppointmentSlots(user_id):
    clinicAvailibility = User.get_user_clinic_availibility(where={'user_id': user_id})
    booked_slot_obj = User.get_booked_slot(user_id, ['appointment_datetime'])
    booked_slot_list = []
    print("Booked list")

    if booked_slot_obj:
        for bs in booked_slot_obj:
            print(bs.appointment_datetime)
            booked_slot_list.append(bs.appointment_datetime.strftime("%d-%m-%Y %H:%M"))
    print(booked_slot_list)
    ca_header = {}

    ca_slot = {}
    day_available = {}
    if clinicAvailibility:
        for ca in clinicAvailibility:
            day_available[ca.day] = ca

        # datetime object containing current date and time
        now = dt.datetime.now()
        # dd/mm/YY H:M:S
        today_date = now.strftime("%d-%m-%Y")
        print("date and time =", today_date)
        no_of_days = 14
        i = 0

        while i < no_of_days:
            date_then = now + dt.timedelta(days=i)

            day_then = date_then.strftime("%A").lower()
            date_then = date_then.strftime("%d-%m-%Y")
            i += 1

            day = day_available[day_then].day

            start_time = day_available[day_then].start_time
            end_time = day_available[day_then].end_time
            duration = str(day_available[day_then].duration)
            is_available = day_available[day_then].is_available
            slots = User.time_slots(start_time, end_time, duration)
            slot_available = len(slots)
            class_css = ''
            class_css_slot = ''
            if today_date == date_then:
                class_css = 'active'
                class_css_slot = 'in active'

            key = str(date_then)+"_"+str(user_id)

            day_time = {}
            after_noon = dt.datetime.strptime('12:00', '%H:%M')
            evening = dt.datetime.strptime('16:00', '%H:%M')
            day_time['morning'] = []
            day_time['afternoon'] = []
            day_time['evening'] = []
            slot_count = 0
            for st in slots:
                s_time = dt.datetime.strptime(st, '%H:%M')
                s_datetime = "{0} {1}".format(date_then, st)
                if s_datetime not in booked_slot_list:
                    slot_count = slot_count +1
                    if s_time < after_noon:
                        day_time['morning'].append(st)
                    if s_time >= after_noon and s_time < evening:
                        day_time['afternoon'].append(st)
                    if s_time >= evening:
                        day_time['evening'].append(st)
            ca_slot[date_then] = {'day_time': day_time, 'class': class_css_slot, 'day': day,
                                       'is_available': is_available, 'user_id': user_id}

            ca_header[date_then] = {'day': day, 'slot_available': slot_count, 'class': class_css,
                                    'is_available': is_available, 'user_id': user_id}

    return ca_header, ca_slot


@loggedin
def paymentSave(request):
        print(request.POST)
        session_cart = request.session.get('cart', {})
        loggedin_user_data = request.session.get('loggedin_user', {})
        print(loggedin_user_data)
        print('inside save payment')
        appointment_id = request.session['appointment_id']
        payment_date = date.today().strftime("%Y-%m-%d 00:00:00")
        payment_mode='online'
        payment_amount = session_cart['final_amount']
        payment_status=request.POST['payment_status']
        coupon_code = session_cart['coupon_code'] if 'coupon_code' in session_cart else None
        is_active=1
        txn_id=str(request.POST.get('txn_id')),
        user_id=loggedin_user_data['id']
        print(txn_id)
        userPayment=User_Payment(
        appointment_id=appointment_id,payment_date=payment_date,payment_mode=payment_mode,
        payment_status=payment_status,is_active=is_active,txn_id=txn_id,user_id=user_id,
            payment_amount=payment_amount, coupon_code= coupon_code
        )
        try:
            userPayment.save()
            print("i m here")
            if payment_status == 'paid':
                print("paid")
                if 'appointment_id' in request.session:
                    print(request.session['appointment_id'])
                    user_apt_update = User.update_user_appointment_status(request.session['appointment_id'],2)
                    print(user_apt_update)
                    print(request.session)
                    del request.session['appointment_id']
            return JsonResponse({'resp': "success"})
        except Exception as e:
            print (e)

            return JsonResponse({'resp': "failed"})


@loggedin
@csrf_exempt
def appointmentSave(request):
    print(request)
    where = {}
    user_appintment = {}
    user_appintment['patient_id'] = request.session['loggedin_user']['id']
    user_appintment['user_clinic_id'] = "1"
    date_obj, db_time = date_format(request.session['cart']['apt_date']+ " "+request.session['cart']['apt_time'], '%d-%m-%Y %H:%M', '%Y-%m-%d %H:%M')
    user_appintment['appointment_datetime'] = db_time
    user_appintment['appointment_type'] = "at clinic"
    user_appintment['appointment_status'] = 1
    user_appintment['payment_type'] = "online"
    user_appintment['is_active'] = 1
    user_appintment['user_id'] = int(request.session['cart']['doctor_id'])
    where['user_appointment_id'] = request.session['appointment_id'] if 'appointment_id' in request.session else None
    user_appointment_id = User.add_or_update_user_appointment(user_appintment, where)
    if user_appointment_id:
        request.session['appointment_id'] = user_appointment_id
        return JsonResponse({'resp': "success"})
    else:
        return JsonResponse({'resp': "failed"})



@loggedin
def patientAppointmentView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {"is_active": 1, "user_id":user_data['id']}
    appointment_list = User.get_user_appointment(where=where)
    patient_data = []
    apt_status_lookup = {}
    apt_status_lookup[2] = "Appointment has been booked, please confirm/modify/cancel!"
    apt_status_lookup[3] = "Appointment has been cancelled by patient!"
    apt_status_lookup[4] = "Appointment has been modified by patient, please confirm/modify/cancel."
    apt_status_lookup[5] = "Appointment has been confirmed by you!"
    apt_status_lookup[6] = "Appointment has been modified by you!"
    apt_status_lookup[7] = "Appointment has been cancelled by you!"
    apt_status_lookup[8] = "Consultation is completed!"
    apt_status_lookup[9] = "Referred by you!"
    if appointment_list:
        for apt in appointment_list:
            print(apt)
            d = {}
            d['info'] = User.get_user({"user_id":apt.patient_id})

            d['payment'] = User.get_user_payment(where={"appointment_id": apt.user_appointment_id})
            d['address'] = User.get_user_address({"user_id":apt.patient_id})
            d['apt'] = apt
            d['apt_status'] = apt_status_lookup.get(apt.appointment_status, "")
            if apt.appointment_status == 9:
                print("I am inside 9")
                referred_data = User.get_dr_patient_refer({"user_appointment_id": apt.user_appointment_id})
                referred_to_dr_id = referred_data[0].user_to
                referred_dr_info = User.get_user({"user_id": referred_to_dr_id})
                d['apt_status'] = "Referred to {0} {1} ".format(referred_dr_info.user_first_name,
                                                                referred_dr_info.user_last_name)

            print(d['apt_status'])
            patient_data.append(d)
    return render(request, "web_app/appointment-dr.html", {'user_data':user_data, 'patient_data' : patient_data})


@loggedin
def myAppointmentView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {"is_active": 1, "patient_id":user_data['id']}
    appointment_list = User.get_user_appointment(where=where)
    patient_data = []
    apt_status_lookup = {}
    apt_status_lookup[2] = "Appointment has been booked, please confirm/modify/cancel!"
    apt_status_lookup[3] = "Appointment has been cancelled by patient!"
    apt_status_lookup[4] = "Appointment has been modified by patient, please confirm/modify/cancel."
    apt_status_lookup[5] = "Appointment has been confirmed by you!"
    apt_status_lookup[6] = "Appointment has been modified by you!"
    apt_status_lookup[7] = "Appointment has been cancelled by you!"
    apt_status_lookup[8] = "Consultation is completed!"
    apt_status_lookup[9] = "Referred by you!"
    if appointment_list:
        for apt in appointment_list:
            print(apt)
            d = {}
            d['info'] = User.get_user({"user_id":apt.user_id})

            d['payment'] = User.get_user_payment(where={"appointment_id": apt.user_appointment_id})
            d['address'] = User.get_user_address({"user_id":apt.user_id})
            d['apt'] = apt
            d['apt_status'] = apt_status_lookup.get(apt.appointment_status, "")
            if apt.appointment_status == 9:
                print("I am inside 9")
                referred_data = User.get_dr_patient_refer({"user_appointment_id": apt.user_appointment_id})
                referred_to_dr_id = referred_data[0].user_to
                referred_dr_info = User.get_user({"user_id": referred_to_dr_id})
                d['apt_status'] = "Referred to {0} {1} ".format(referred_dr_info.user_first_name,
                                                                referred_dr_info.user_last_name)

            print(d['apt_status'])
            patient_data.append(d)
    return render(request, "web_app/appointment-patient.html", {'user_data':user_data, 'patient_data' : patient_data})


@loggedin
def patientReferView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {"is_active": 1, "user_to":user_data['id']}
    patient_list = User.get_dr_patient_refer(where=where)
    patient_data = []
    if patient_list:
        for p in patient_list:
            print(p.user_appointment_id)
            d = {}
            d['ref'] = p
            referred_by_dr_id = p.user_from
            referred_by_dr_info = User.get_user({"user_id": referred_by_dr_id})
            d['apt_status'] = "Referred By {0} {1} ".format(referred_by_dr_info.user_first_name, referred_by_dr_info.user_last_name)
            d['info'] = User.get_user({"user_id":p.patient_id})
            d['address'] = User.get_user_address({"user_id":p.patient_id})
            print(d)
            patient_data.append(d)
    print(patient_data)
    return render(request, "web_app/referred-patient.html", {'user_data':user_data, 'patient_data' : patient_data})


@loggedin
def doctorReferView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {"is_active": 1, "patient_id":user_data['id']}
    user_list = User.get_dr_patient_refer(where=where)
    data = []
    if user_list:
        for p in user_list:
            print(p.user_appointment_id)
            d = {}
            d['ref'] = p
            referred_by_dr_id = p.user_from
            referred_by_dr_info = User.get_user({"user_id": referred_by_dr_id})
            referred_to_dr_info = User.get_user({"user_id": p.user_to})
            d['referred_by'] = referred_by_dr_info
            d['referred_to'] = referred_to_dr_info
            d['info'] = User.get_user({"user_id":p.patient_id})
            d['address'] = User.get_user_address({"user_id":p.patient_id})
            print(d)
            data.append(d)
    print(data)
    return render(request, "web_app/referred-doctor.html", {'user_data':user_data, 'patient_data' : data})




@csrf_exempt
@loggedin
def updateAppointmentAjax(request):
    user_data = request.session.get('loggedin_user', {})
    print(request.POST)

    appt_status = {}

    appt_status['confirm-apt'] = 5
    appt_status['modify-apt'] = 6
    appt_status['cancel-apt'] = 7
    appt_status['consult-apt'] = 8
    appt_status['dr-refer'] = 9
    action = request.POST['action']
    status = appt_status[action]
    appointment_id = request.POST['appointment_id']
    modified_datetime = request.POST.get('modified_datetime', None)
    if modified_datetime:
        User.update_user_appointment_datetime(appointment_id, modified_datetime)

    if action == 'dr-refer':
        data = {}
        data['user_appointment_id'] = appointment_id
        data['patient_id'] = request.POST.get('patient_id', None)
        data['user_from'] = user_data['id']
        data['user_to'] = request.POST.get('referred_to_dr_id', None)
        data['refer_notes'] = request.POST.get('refer_notes', '')
        User.set_dr_patient_refer(data)

    User.update_user_appointment_status(appointment_id, status)

    return JsonResponse({'resp': "success"})


@csrf_exempt
@loggedin
def drReferPatientView(request):
    user_data = request.session.get('loggedin_user', {})
    print(user_data)
    search_keyword = request.POST.get('search_keyword')
    search_city = request.POST.get('search_city')
    print(search_keyword)
    print(user_data['id'])
    result = User.search_user(search_keyword, search_city, user_data['id'])

    print(result)
    return render(request,"web_app/dr-refer-patient-page.html", {'data':{'keyword':search_keyword, 'city':search_city},'result': result,'user_data':user_data})
    #return render(request, "web_app/search-page.html",{})

@csrf_exempt
@loggedin
def applyCouponAjax(request):

    coupon_code = request.POST.get('coupon', None)
    where = {'coupon_code': coupon_code, 'is_active': 1}
    coupon_data = Coupon.get_coupon(where)
    if coupon_data:
        user_data = request.session.get('loggedin_user', {})
        where = {'user_id':user_data['id'],'coupon_code': coupon_code, 'is_active': 1}
        is_coupon_applied = User.is_coupon_applied(where)
        session_cart ={}
        if not is_coupon_applied:
            where = {'coupon_code':coupon_code, 'is_active': 1}
            coupon_data = Coupon.get_coupon(where)
            session_cart = request.session.get('cart', {})
            amount = session_cart['amount']

            coupon_value = coupon_data.coupon_value
            discounted_amount, discount_amount = calc_disc(amount, coupon_value)
            gst_amount = round((discounted_amount)*.18, 2)
            final_amount = int(discounted_amount)+ gst_amount

            session_cart['coupon_code'] = coupon_code
            session_cart['discount_amount'] = discount_amount
            session_cart['discounted_amount'] = discounted_amount
            session_cart['gst_amount'] = gst_amount
            session_cart['final_amount'] = final_amount

            request.session['cart'] = session_cart
            if 'user_id' in session_cart:
                session_cart.pop('user_id')
            return JsonResponse({'status': 'success', 'result': session_cart})
        else:
            return JsonResponse({'status': 'fail', 'result': 'Coupon already applied'})
    else:
        return JsonResponse({'status':'fail', 'result':'Invalid coupon'})

def calc_disc(amount, disc):
    amount = int(amount)
    if '%' in disc:
        x = int(disc.replace('%',''))
        discount = round((amount*x)/100,2)
    elif '%' not in disc and disc != '0':
        discount = disc
    elif disc == '0':
        discount = amount

    discounted_val = amount - int(discount)
    return discounted_val, discount
    
    



def getPaymentAjax(request):
    return JsonResponse({'amount':request.session['cart']['final_amount']})

def forgotPasswordView(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        user_email = request.POST.get('user_email')
        user = User.get_user({'user_email': user_email, 'user_type_id': user_type, 'is_active': 1})
        if user:
            # Generate and send OTP
            otp_service = OtpService()
            otp = otp_service.generate()
            otp_sent = otp_service.sendEmailOtp(user_email)  # Use sendSmsOtp if needed

            if otp_sent:
                request.session['otp'] = otp
                request.session['otp_user_id'] = user.user_id
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to send OTP'})
        else:
            return JsonResponse({'success': False, 'message': 'Email is not registered'})

    return render(request, "web_app/forgot-password.html")

def validate_otp(request):
    if request.method == 'POST':
        entered_otp = int(request.POST.get('entered_otp'))
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            request.session['forgot_user'] = {'id':request.session['otp_user_id']}
            del request.session['otp']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return render(request,"web_app/reset-password.html")

def resetPasswordView(request):
    user_data = request.session.get('loggedin_user', {})
    loggedin_user_data = user_data
    if not user_data:
        user_data = request.session.get('forgot_user', {})
    if not user_data:
        return redirect('/login')

    if request.method == 'POST':
        user_id = user_data['id']
        new_password = request.POST.get('new_password')
        user = User.get_user({"user_id": user_id})
        if user:
            user.password = new_password
            user.save()
            if 'forgot_user' in request.session:
                del request.session['forgot_user']
            if 'loggedin_user' in request.session:
                del request.session['loggedin_user']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'User not found'})

    return render(request, "web_app/reset-password.html", {'user_data':loggedin_user_data})

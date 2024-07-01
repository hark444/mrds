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
from services.ReferService import ReferService
from django.shortcuts import render
# Create your views here.

User = UserService()
Refer = ReferService()
# Create your views here.

def loggedin(fun):
    def inner(request, *args, **kwargs):
        if 'loggedin_user' not in request.session:
            return redirect('/refer/login')
        else:
            return fun(request, *args, **kwargs)
    return inner

def logout(request):
    try:
        del request.session['loggedin_user']
    except:
        return redirect('/refer/login')
    return redirect('/refer/login')


def loginView(request):
    if 'loggedin_user' in request.session:
        del request.session['loggedin_user']
    return render(request,"refer_app/login.html", {'user_data': {}})


@loggedin
def dashboardView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {'referred_by': user_data['id']}
    refers = Refer.get_all_refers(where)
    print(refers)
    print(refers)
    refer_list = []

    for refer in refers:
        refer_data = {}

        user_to = User.get_user({'user_id': refer.referred_to})
        user_by = User.get_user({'user_id': refer.referred_by})
        refer_data['refer_to'] = user_to.user_first_name + " " + user_to.user_last_name
        refer_data['refer_by'] = user_by.user_first_name + " " + user_by.user_last_name
        refer.status = "New"
        existing_user = User.get_user({'user_email': refer.email, 'user_type_id': 1, 'is_active': 1})
        if existing_user:
            refer.status = "Registered"
        refer_data['refer'] = refer
        refer_list.append(refer_data)
    return render(request,"refer_app/dashboard.html", {'user_data':user_data, 'refers':refers, 'refer_list': refer_list})

@csrf_exempt
def ajaxLogin(request):
    print(request.POST)
    req = request.POST
    data = {}
    data['user_name'] = req.get('username')
    data['password'] = req.get('password')
    data['user_type_id'] = 3

    user = User.get_user(data)
    if not user:
        return JsonResponse({'resp': 'User doesn\'t exist' , 'status': 'failed'})

    userdata = {"id":user.user_id,
                "name":user.user_first_name+" "+user.user_last_name,
                "user_type":user.user_type_id}

    request.session['loggedin_user'] = userdata
    #return redirect('home')
    return JsonResponse({'resp': 'redirect', 'status': 'success'})
@loggedin
@csrf_exempt
def ajaxRefer(request):
    user_data = request.session.get('loggedin_user', {})
    referral_code = "DR"+Refer.generate_referral_code()
    req = request.POST

    user = User.get_user({'user_email': req.get('email'), 'user_type_id': 1, 'is_active': 1})
    if user:
        user_id = user.user_id
    else:
        data = {}
        data['user_first_name'] = req.get('first_name')
        data['user_last_name'] = req.get('last_name')
        data['user_email'] = req.get('email')
        data['user_mobile'] = req.get('mobile_number')
        data['user_type_id'] = 1
        data['password'] = req.get('mobile_number')
        data['user_name'] = req.get('email')
        data['referral_code'] = referral_code
        user_id = User.add_user(data)

    data = {}
    data['user_appointment_id'] = 0
    data['patient_id'] = user_id
    data['user_from'] = user_data['id']
    data['user_to'] = 1
    data['refer_notes'] = "Diagnosis: "+req.get('diagnosis', '')+"<br>"+"Treatment: "+req.get('treatment', '')+"<br>"
    User.set_dr_patient_refer(data)


    data = {}
    data['first_name'] = req.get('first_name')
    data['last_name'] = req.get('last_name')
    data['mobile_number'] = req.get('mobile_number')
    data['email'] = req.get('email')
    data['city'] = req.get('city')
    data['diagnosis'] = req.get('diagnosis')
    data['treatment'] = req.get('treatment')
    data['is_active'] = 1
    data['referred_by'] = user_data['id']
    data['referred_to'] = 1
    data['referral_code'] = referral_code
    data['status'] = 1

    refer_id = Refer.add_refer(data)
    if refer_id:
        # patient_name = data['first_name'] + " " + data['last_name']
        # user = User.get_user({'user_email': data['email'], 'user_type_id': 1, 'is_active': 1})
        # if user:
        #     is_existing_user = True
        #     link = request.get_host() + "/login/patient"
        # else:
        #     is_existing_user = False
        #     link = request.get_host() + "/register/patient/" + referral_code
        #Refer.sendEmailRefer(data['email'], patient_name, user_data['name'], link, is_existing_user)
        return JsonResponse({'resp': 'redirect', 'status': 'success'})
    else:
        return JsonResponse({'resp': 'Error while adding', 'status': 'failed'})


     #return redirect('home')


@loggedin
def referView(request):
    user_data = request.session.get('loggedin_user', {})
    return render(request,"refer_app/refer.html", {'user_data':user_data})

def logout(request):
    try:
        del request.session['loggedin_user']
    except:
        return redirect('/refer/login')
    return redirect('/refer/login')

@loggedin
@csrf_exempt
def getPatientView(request):
    req = request.POST
    email = req.get('email')
    data = {}
    user_data = User.get_user({'user_email': email, 'user_type_id':1, 'is_active': 1})
    if user_data:

        data['first_name'] = user_data.user_first_name
        data['last_name'] = user_data.user_last_name
        data['mobile'] = user_data.user_mobile
        user_address = User.get_user_address({'user_id': user_data.user_id, 'is_active': 1})
        data['city'] = ''
        if user_address:
            data['city'] = user_address.city

    else:
        data['first_name'] = ''
        data['last_name'] = ''
        data['mobile'] = ''
        data['city'] = ''

    return JsonResponse({'resp': data, 'status': 'success'})



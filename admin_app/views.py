from django.shortcuts import render
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import redirect
#from admin_app.services.UserService import UserService as AdminUserService
from services.UserService import UserService
from services.CouponService import CouponService
from services.ReferService import ReferService
from django.shortcuts import render

# Create your views here.

User = UserService()
Refer = ReferService()
Coupon = CouponService()

def loggedin(fun):
    def inner(request, *args, **kwargs):
        if 'loggedin_user' not in request.session:
            return redirect('/admin/login')
        else:
            return fun(request, *args, **kwargs)
    return inner

def logout(request):
    try:
        del request.session['loggedin_user']
    except:
        return redirect('/admin/login')
    return redirect('/admin/login')

@loggedin
def homeView(request):
    user_data = request.session.get('loggedin_user', {})
    return render(request,"web_app/home.html", {'user_data':user_data})

def loginView(request):
    if 'loggedin_user' in request.session:
        del request.session['loggedin_user']
    return render(request,"admin_app/login.html", {'user_data': {}})

def registerView(request):
    return render(request,"admin_app/register.html")

@loggedin
def dashboardView(request):
    user_data = request.session.get('loggedin_user', {})
    return render(request,"admin_app/dashboard.html", {'user_data':user_data})

@loggedin
def doctordView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {'user_type_id': 3}
    users = User.get_all_users(where)
    usersList = []
    print(users)
    for user in users:
        refer_count = Refer.get_refer_count({'referred_by': user.user_id})
        user.count = refer_count

        address = User.get_user_address({'user_id': user.user_id})
        user.address = address.city if address else ""
        usersList.append(user)
    print(usersList)
    return render(request,"admin_app/doctor.html", {'users': usersList, 'user_data':user_data})

@loggedin
def ptView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {'user_type_id': 2}
    users = User.get_all_users(where)
    usersList = []
    print(users)
    for user in users:
        address = User.get_user_address({'user_id': user.user_id})
        user.address = address.city if address else ""
        #print (user.address)
        usersList.append(user)
    print(usersList)
    return render(request,"admin_app/pt.html", {'users': usersList, 'user_data':user_data})

@loggedin
def patientView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {'user_type_id': 1}
    users = User.get_all_users(where)
    usersList = []
    print(users)
    for user in users:
        address = User.get_user_address({'user_id': user.user_id})
        user.address = address.city if address else ""
        usersList.append(user)
    print(usersList)
    return render(request,"admin_app/patient.html", {'users': usersList, 'user_data':user_data})

@loggedin
def referralView(request):
    user_data = request.session.get('loggedin_user', {})
    #where = {'referred_to': user_data['id']}
    where = {}
    refers = Refer.get_all_refers(where)
    print(refers)
    refer_list = []

    for refer in refers:
        refer_data = {}
        refer_data['refer'] = refer
        user_to = User.get_user({'user_id': refer.referred_to})
        user_by = User.get_user({'user_id': refer.referred_by})
        refer_data['refer_to'] = user_to.user_first_name + " " + user_to.user_last_name
        refer_data['refer_by'] = user_by.user_first_name + " " + user_by.user_last_name

        user = User.get_user({'user_email': refer.email, 'user_type_id': 1, 'is_active': 1})
        refer_data['user_action'] = "Add"
        refer_data['user_id'] = 0
        if user:
            refer_data['user_action'] = "Refer"
            refer_data['user_id'] = user.user_id
        refer_list.append(refer_data)
    return render(request,"admin_app/referrals.html", {'user_data':user_data, 'refers':refers, 'refer_list': refer_list})

@loggedin
def couponsView(request):
    user_data = request.session.get('loggedin_user', {})
    where = {}
    coupons = Coupon.get_all_coupons(where)
    print(coupons)
    couponList =[]
    for coupon in coupons:
        couponList.append(coupon)
    print(couponList)

    return render(request,"admin_app/coupons.html",{ 'coupons': coupons,'user_data':user_data})

def logout(request):
    try:
        del request.session['loggedin_user']
    except:
        return redirect('/login')
    return redirect('/login')

@csrf_exempt
def ajaxLogin(request):
    print(request.POST)
    req = request.POST
    data = {}
    data['user_name'] = req.get('username')
    data['password'] = req.get('password')
    data['user_type_id'] = 4

    user = User.get_user(data)
    if not user:
        return JsonResponse({'resp': 'User doesn\'t exist' , 'status': 'failed'})

    userdata = {"id":user.user_id,
                "name":user.user_first_name+" "+user.user_last_name,
                "user_type":user.user_type_id}

    request.session['loggedin_user'] = userdata
    #return redirect('home')
    return JsonResponse({'resp': 'redirect', 'status': 'success'})

@csrf_exempt
def ajaxRegister(request):
    print(request.POST)
    req = request.POST
    data = {}
    data['user_name'] = req.get('username')
    data['password'] = req.get('password')
    data['user_first_name'] = req.get('first_name')
    data['user_last_name'] = req.get('last_name')
    data['user_mobile'] = req.get('mobile')
    data['user_email'] = req.get('email')
    data['user_type_id'] = req.get('user_type')

    user_id = User.add_user(data)
    if not user_id:
        return JsonResponse({'resp': 'User doesn\'t exist' , 'status': 'failed'})

     #return redirect('home')
    return JsonResponse({'resp': 'redirect', 'status': 'success'})



@csrf_exempt
def ajaxAddCoupon(request):
    print(request.POST)
    req = request.POST
    data = {}
    data['coupon_name'] = req.get('coupon_name')
    data['coupon_code'] = req.get('coupon_code')
    data['coupon_value'] = req.get('coupon_value')
    data['coupon_description'] = req.get('coupon_description')
    coupon_id = Coupon.add_coupon(data)
    if not coupon_id:
        return JsonResponse({'resp': 'coupon doesn\'t exist', 'status': 'failed'})
    return JsonResponse({'resp': 'redirect', 'status': 'success'})


@csrf_exempt
def ajaxUpdateCoupon(request):
    print(request.POST)
    req = request.POST
    data = {}
    where = {}
    data['is_active']=req.get('is_active')
    where['coupon_id']= req.get('coupon_id')
    Coupon.update_coupon(data,where)
    return JsonResponse({'resp': 'redirect', 'status': 'success'})
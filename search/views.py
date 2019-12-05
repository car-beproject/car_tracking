from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib import messages
from django.template import RequestContext
from .models import *
# Create your views here.
global l_query,u_name_query, u_role_query

l_query = New_location_db.objects.all()

def login(request):
    return render(request, "login.html",{'u_name':request.session.get('u_name')})

def login_action(request):
    u_name_query= request.POST.get('u_name')
    p_word_query= request.POST.get('p_word')
    s_query = Vehicle.objects.all()
    u_query = AuthUser_db.objects.all().filter(u_name = u_name_query).filter(p_word = p_word_query)

    if u_query:
        for u in u_query:
            request.session['role']=(u.u_role)
        request.session['u_name']=u_name_query

        return render(request,"index.html", {'s_query': s_query, 'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else :
        fail="login failed"
        return render(request,"login.html",{'fail':fail})

def logout(request):
    del request.session['u_name']
    del request.session['role']
    return render(request, 'login.html')

def index(request):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        return render(request,"index.html",{'s_query':s_query, 'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")

def search(request):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        l_query = New_location_db.objects.all()
        license_query = request.GET.get("license_plate")
        if(license_query is not None):
            license_query=license_query.replace(" ", "").upper()
        location_query = request.GET.get("location")
        start_date_query = request.GET.get("start_date")
        end_date_query = request.GET.get("end_date")
        
        if location_query=="All":location_query=""
        if start_date_query=="":start_date_query="1980-01-01"
        if end_date_query=="":end_date_query="2200-01-01"
        if start_date_query > end_date_query:
            info ='Date should be in proper order!!!'
            return render(request,"index.html",{'l_query':l_query,'info':info})
        if license_query or location_query or start_date_query or end_date_query:
            s_query = s_query.filter(license_number__icontains = license_query).filter(location__icontains = location_query).filter(date__range = (start_date_query, end_date_query))    
            if s_query:
                return render(request, "index.html",{'s_query': s_query,'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
            else:
                return render(request, "index.html", {'s_query': s_query,'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
        return render(request, "index.html",{'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")

def vehicle_details(request, id):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        s_query = s_query.filter(id__icontains = id)
        return render(request, "vehicle_details.html",{'s_query': s_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
def camera_details(request):
    if request.session.get('u_name'):
        c_query = CameraDb.objects.all()
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()

        return render(request, "camera_details.html",{'c_query': c_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name'), 'new_location': new_location_query, 'new_camera_type':new_camera_type_query })
    else:
        return render(request,"login.html")
        
def search_camera(request):
    if request.session.get('u_name'):
        ip_address_query=request.GET.get("ip_add")
        location_query=request.GET.get("location")
        if location_query=="All":
            location_query=""
        camera_type_query=request.GET.get("camera_type")
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()

        c_query= CameraDb.objects.all()
        c_query = c_query.filter(ip_address__icontains=ip_address_query).filter(camera_type__icontains=camera_type_query).filter(location__icontains=location_query)
        return render(request, "camera_details.html",{'u_role':request.session.get('role') ,'u_name':request.session.get('u_name') ,'c_query': c_query, 'location': location_query, 'camera_type':camera_type_query , 'new_location': new_location_query, 'new_camera_type':new_camera_type_query})
    else:
        return render(request,"login.html")
        
## camera add
def add_cam(request):
    if request.session.get('u_name'):
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()

        return render(request,'add_cam.html', {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name'), 'new_location': new_location_query, 'new_camera_type':new_camera_type_query })
    else:
        return render(request,"login.html")
        
def add_cam_action(request):
    if request.session.get('u_name'):
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()
        c_query = CameraDb.objects.all()

        ip_address_query = request.GET.get("ip_address")
        location_query = request.GET.get("location").upper()
        camera_type_query = request.GET.get("camera_type")
        q=CameraDb.objects.all().filter(ip_address__exact=ip_address_query)
        
        if q:
            error="Camera IP is already in use!!!"
            return render(request,'add_cam.html',{'u_role':request.session.get('role') , 'u_name':request.session.get('u_name'), 'new_location': new_location_query, 'new_camera_type':new_camera_type_query,'error':error })
        if ip_address_query is not None and camera_type_query is not None and location_query is not None:
            new_camera = CameraDb(ip_address=ip_address_query, location=location_query, camera_type=camera_type_query)
            new_camera.save()
        
        return render(request, 'camera_details.html', {'c_query':c_query,'u_role':request.session.get('role') , 'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
def new_details(request):
    if request.session.get('u_name'):
        return render(request,"new_details.html", {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
def new_details_action(request):
    if request.session.get('u_name'):
        new_location_query = request.GET.get("new_location").upper()
        new_camera_type_query = request.GET.get("new_camera_type").upper()
        if new_location_query is not None :
            new_location = New_location_db(location=new_location_query)
            new_location.save()
        if new_camera_type_query is not None:
            new_camera_type = New_camera_type_db(camera_type=new_camera_type_query)
            new_camera_type.save()
        return render(request, 'index.html', {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
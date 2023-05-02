from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from django.contrib.sessions.backends.db import SessionStore

import sms

import random
import string

import json

from datetime import timedelta

from .models import User

from django.contrib.auth.models import User

from .forms import RegPhoneForm, RegSMSForm, RegLoginForm

session = SessionStore()

session.set_expiry(
    timedelta(minutes=30)
)

@csrf_exempt
def send_sms(req : HttpRequest):
    if(req.method == 'POST'):

        data = json.loads(req.body.decode())

        f = RegPhoneForm(data)

        if f.is_valid():    
            ver_code   = ''.join(random.choices(string.ascii_uppercase, k=5))

            with sms.get_connection() as connection:

                session['ver_code'] = ver_code

                num = sms.Message(
                    ver_code, '+421932132131', [{data['phone']}],
                    connection=connection
                ).send()

            if num > 0 : code = 200
            else : code = 303

        else :
            print(f.errors.as_data())
            code = 403    
        
        return JsonResponse(
                    {'code' : code}
        )
   
@csrf_exempt
def check_sms(req : HttpRequest):
    if(req.method == 'POST'):
        data = json.loads(req.body.decode())

        f = RegSMSForm(data)

        if f.is_valid():
            if data['ver_code'] == session['ver_code']: code = 200
            else : code = 403
        else : code = 401

        print(session['ver_code'])
        
        return JsonResponse(
            {'code' : code}
        )

@csrf_exempt
def check_username(req : HttpRequest):
    if(req.method == 'POST'):
        data = json.loads(req.body.decode)
        
        f = RegLoginForm(data)

        if f.is_valid():
            _username = data.get('username')

            user = User.objects.all()

            userquery = user.filter(username = _username).query

            userquery = list(userquery)

            if len(userquery) > 0 : code =  300
            else : code = 200
        else : 
            code = 401

        return JsonResponse(
            {'exists' : code}
        )


@csrf_exempt
def create_user(req : HttpRequest):
    if(req.method == 'POST'):
        d = json.loads(req.body.decode())

        user = User.objects.create_user(
            username=d.get('name'),
            email = d.get('email'),
            password = d.get('password'),
            first_name = d.get('name'),
            last_name = d.get('lastName'),
            phone = d.get('phone')
        )

        return JsonResponse(
            {
                'created' : user.save()
            }
        )
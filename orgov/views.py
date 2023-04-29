from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from django.contrib.sessions.backends.db import SessionStore

import sms

import random
import string

import json

from datetime import timedelta

from .models import User

session = SessionStore()

@csrf_exempt
def send_sms(req : HttpRequest):
    if(req.method == 'POST'):

        d = json.loads(req.body.decode())
        phone = d.get('phone')

        ver_code = ''.join(random.choices(string.ascii_uppercase, k=5)) 

        with sms.get_connection() as connection:

            session['ver_code'] = ver_code

            num = sms.Message(
                ver_code, '+421932132131', [f'{phone}'],
                connection=connection
            ).send()

            print(num)

            if num > 0 :

                session.set_expiry(
                    timedelta(minutes=30)
                )

                req.session['ver_code'] = ver_code

                return JsonResponse(
                    {'code' : 200}
                )
            
            else :
                return JsonResponse(
                    {'code' : 403}
                )
   
@csrf_exempt
def check_sms(req : HttpRequest):
    if(req.method == 'POST'):
        d = json.loads(req.body.decode())

        ver_code : str = d.get('sms')
        
        ver_code = ver_code.upper()

        print(session['ver_code'])
        
        if ver_code == session['ver_code']:
            return JsonResponse(
                {'code' : 200}
            )
        else : 
            return JsonResponse(
                {'code' : 403}
            )

@csrf_exempt
def create_user(req : HttpRequest):
    if(req.method == 'POST'):
        d = json.loads(req.body.decode())

        user = User.objects.create(
            name = d.get('name'),
            lastName = d.get('lastName'),
            email = d.get('email'),
            phone = d.get('phone'),
            username = d.get('username'),
            password = d.get('password'),
            authorized = d.get('authorized')
        )

        return JsonResponse(
            {
                'created' : user.save()
            }
        )
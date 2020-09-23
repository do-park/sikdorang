import time, json, requests, base64, hmac, hashlib
from decouple import config

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import UserPhoneCheck

@api_view(['GET'])
def phone(request, phone_num):
    user_phone = UserPhoneCheck.objects.update_or_create(phone_number=phone_num)[0]
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    url = "https://sens.apigw.ntruss.com"
    requestUrl = "/sms/v2/services/"
    requestUrl2 = "/messages"
    serviceId = config("SERVICE_ID")
    access_key = config("ACCESS_KEY")

    uri = requestUrl + serviceId + requestUrl2
    apiUrl = url + uri

    def make_signaure(uri, access_key):
        secret_key = config("SECRET_KEY")
        secret_key = bytes(secret_key, 'UTF-8')
        method = "POST"
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signigKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signigKey

    messages = { "to" : user_phone.phone_number }
    body = {
        "type" : "SMS",
        "contentType" : "COMM",
        "from" : "01076338540",
        "subject" : "subject",
        "content" : "[식도랑] 인증 번호 [{}]를 입력하세요.".format(user_phone.auth_number),
        "messages" : [messages]
    }
    body2 = json.dumps(body)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": make_signaure(uri, access_key)
    }

    res = requests.post(apiUrl, headers=headers, data=body2)
    print(res.json())
    context = {
        'message': 'OK',
    }
    return JsonResponse(context)

@api_view(['POST'])
def phone_auth(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    result = UserPhoneCheck.objects.filter(
        phone_number=request.data["phone_num"],
        auth_number=request.data["auth_num"]
    )
    message = 'fail'
    if result:
        message = 'success'
        user.phone_number = request.data["phone_num"]
        user.save()
        result.delete()
    context = {
        'message': message
    }
    return JsonResponse(context)
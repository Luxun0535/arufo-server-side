from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
from urllib.parse import urlencode
from storeshop.sign import build_mysign
from arufo_server_side import  settings
from django.contrib.auth.models import User
from storeshop.models import Consumption,Exchange,User_info,User_prop
import datetime
import json
# Create your views here.

def sign ( request ):
    if request.method == 'POST':
        try:
            dataFromClientEncoded = request.body.decode("utf-8")
            data = json.loads(dataFromClientEncoded)
        except Exception as e:
            return HttpResponse(type(e))
        tn = data['tn']
        subject = data['subject']
        body = data['body']
        total_fee = data['total_fee']
        userid = data['userid']
        score=total_fee
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        status=1 #充值进行中
        print(userid)
        consumption=Consumption(orderid=tn,userid=userid,total=total_fee,score=score,time=time,status=1)
        consumption.save()
        sign = build_mysign(tn, subject, body, total_fee)
        dataToClientDecoded = {
            "sign":sign,
            "sign_type":settings.ALIPAY_SIGN_TYPE,
        }
        dataToClientEncoded = json.dumps(dataToClientDecoded)

        return HttpResponse(dataToClientEncoded )

def notify_verify(request):
    if request.method == 'POST':
        try:
            dataFromClientEncoded = request.body.decode("utf-8")
            data = json.loads(dataFromClientEncoded)
        except Exception as e:
            return HttpResponse(type(e))
        tn = data['tn']
        subject = data['subject']
        body = data['body']
        total_fee = data['total_fee']
        mysign = build_mysign(tn, subject, body, total_fee)
        if mysign != request.POST.get('sign'):
            return HttpResponse ("fail")


        params = {}
        params['partner'] = settings.ALIPAY_PARTNER
        params['notify_id'] = data['notify_id']

        gateway = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
        verify_result = urlopen(gateway, urlencode(params)).read()
        if verify_result.lower().strip() != 'true':
            return HttpResponse ("fail")

        trade_status = data['trade_status']
        if trade_status == 'TRADE_FINISHED':
            consumptions=Consumption.objects.filter(orderid=tn)
            if consumptions.exits():
                consumption=consumptions[0]
                userid=consumption.userid
                score=consumption.score
                consumption.status=2
                consumption.save()
                userinfos=User_info.objects.filter(userid=userid)
                if userinfos.exists():
                    userinfo=userinfos[0]
                    userinfo.score+=score
                    userinfo.save()
                else:
                    userinfo=User_info.objects.filter(userid=userid,score=score)
                    userinfo.save()
            return HttpResponse("success")
        else:
            consumptions=Consumption.objects.filter(orderid=tn)
            if consumptions.exists():
                consumption=consumptions[0]
                consumption.status=0
                consumption.save()
            return HttpResponse("success")
    else:
        return HttpResponse("fail")

def Exchange_prop(request):
    try:
        dataFromClientEncoded = request.body.decode("utf-8")
        data = json.loads(dataFromClientEncoded)
    except Exception as e:
        return HttpResponse(type(e))
    userid=data['userid']
    prop=data['prop']
    amount=data['amount']
    score=int(data['score'])
    userinfos=User_info.objects.filter(userid=userid)
    if userinfos.exists():
        userinfo=userinfos[0]
        score1=int(userinfo.score)
        if score1>=score:
            userinfo.score=score1-score
            userinfo.save()
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
            exchange=Exchange(userid=userid,prop=prop,amount=amount,score=score,time=time)
            exchange.save()
            user_props=User_prop.objects.filter(userid=userid,prop=prop)
            if user_props.exists():
                user_prop=user_props[0]
                user_prop.amout+=amount
                user_prop.save()
            else:
                user_prop=User_prop(userid=userid,prop=prop,amount=amount)
                user_prop.save()
            return HttpResponse("success")
        else:
            return HttpResponse("noscore")
    else:
        return HttpResponse("noscore")

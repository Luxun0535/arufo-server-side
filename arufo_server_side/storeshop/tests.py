from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
# Create your tests here.
from django.test import TestCase, Client, SimpleTestCase
import json
from storeshop.models import Consumption,Exchange,User_info,User_prop
import datetime

class SignTestCase(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_sign(self):
        user=User(id='101',username='1',password='123')
        user.save()
        request_data = {
            'tn':"123",
            'subject':'subject',
            'body':'body',
            'total_fee':'500',
            'userid':'101',
        }
        response = self.client.post('/store/sign/', json.JSONEncoder().encode(request_data), 'application/json')
        print(response.content)
        self.assertEqual(response.status_code, 200)

class Notify_verifyTsetCase(SimpleTestCase):

    def setUp(self):
        self.client = Client()
    def test_notify(self):
        request_data = {
            'tn':"123",
            'subject':'subject',
            'body':'body',
            'total_fee':'50',
            'sign': '',
            'notify_id':'',
            'trade_status':'',
        }
        user=User(id='102',username='12',password='123')
        user.save()
        consumption=Consumption(orderid="123",userid='102',total="50",score='500',status=1)
        consumption.save()
        response = self.client.post('/store/notify_verify/', json.JSONEncoder().encode(request_data), 'application/json')
        data=response.content.decode('utf-8')
        self.assertEqual(data, "fail")

class ExchangeTestCase(SimpleTestCase):
    def setUp(self):
        self.client = Client()
    def test_exchange(self):
        user=User(id='102',username='123',password='123')
        user.save()
        request_data = {
            'userid':'102',
            'prop':"123",
            'amount':'2',
            'score':'300',
        }
        response = self.client.post('/store/Exchange_prop/', json.JSONEncoder().encode(request_data), 'application/json')
        data=response.content.decode('utf-8')
        self.assertEqual(data, "noscore")

        userinfo=User_info(userid='102',score="500")
        userinfo.save()
        response2 = self.client.post('/store/Exchange_prop/', json.JSONEncoder().encode(request_data), 'application/json')
        data2=response2.content.decode('utf-8')
        self.assertEqual(data2, "success")

        user=User(id='103',username='1234',password='123')
        user.save()
        userinfo=User_info(userid='103',score="100")
        userinfo.save()
        request_data = {
            'userid':'103',
            'prop':"123",
            'amount':'2',
            'score':'300',
        }
        response3 = self.client.post('/store/Exchange_prop/', json.JSONEncoder().encode(request_data), 'application/json')
        data3=response3.content.decode('utf-8')
        self.assertEqual(data3, "noscore")

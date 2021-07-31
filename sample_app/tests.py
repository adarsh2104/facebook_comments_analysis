from django.test import TestCase
from django.test import RequestFactory
from .views import ClassView
import json

class SampleTest(TestCase):
    def test_sample_1(self):
        data = {"name":'ash3'}
        request = RequestFactory().post("/Class",data=data)
        response = ClassView().post(request)
        response_date = json.loads(response.content.decode('UTF-8'))
        assert response.status_code == 201
        assert  response_date.get('id',False)== 1
       




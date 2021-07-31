from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
import json
from .models import  SampleModel
from .serializer import SampleSerializer





def function_view(request,id=''):
    response = {}
    if id.isdigit():
        instance = SampleModel.objects.get(pk=id)
        serializer = SampleSerializer(instance=instance)
        response = serializer.data
    return HttpResponse(json.dumps(response),content_type='application/json')

def show_new_data_form(request):
    if request.method == 'GET':
        return render(request,'new_form.html')
 

class ClassView(APIView):
    def get(self,request):
        instance = SampleModel.objects.get(pk=1)
        serializer = SampleSerializer(instance=instance)
        return HttpResponse(json.dumps(serializer.data),content_type='application/json')
    def post(self,request):
        data = request.POST
        serializer = SampleSerializer(data=data)
        if serializer.is_valid():
            object = serializer.save()
            response = {'id':object.pk}
            status = 201
        else:
            response = {'errors':serializer.errors}
            status = 400
        return HttpResponse(json.dumps(response),content_type='application/json',status=status)
            

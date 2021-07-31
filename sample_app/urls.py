from django.urls import path,include
from .views import function_view,ClassView,show_new_data_form

urlpatterns = [

 path('function/<str:id>', function_view, name='function_view'),
 path('class',ClassView.as_view(),name='class_views'),
 path('new',show_new_data_form,name='show_new_data_form')
]




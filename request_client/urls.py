from django.urls import path,include
from .views import ClassView

urlpatterns = [

 path('class/<str:query>',ClassView.as_view(),name='class_views'),
]




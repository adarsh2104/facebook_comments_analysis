from django.urls import path,include
from .views import ClassView


urlpatterns = [

 path('search/<str:query>',ClassView.as_view(),name='search_views'),
 path('suggest/',ClassView.as_view(),name='search_views'),

]




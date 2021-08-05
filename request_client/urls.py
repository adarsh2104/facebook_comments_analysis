from django.urls import path, include
from .views import SearchView,HomeView

urlpatterns = [
    path('search/<str:query>', SearchView.as_view(), name='search_views'),
    path('suggest/', SearchView.as_view(), name='search_views'),
    path('',HomeView.as_view(),name='home_view')
]

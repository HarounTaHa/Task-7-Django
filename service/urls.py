from django.urls import path
from .views import PlanDetail, VendorList,VendorDetail

urlpatterns = [
    path('vendor/', VendorList.as_view()),
    path('vendor/<str:mac>/', VendorDetail.as_view()),
    path('plan/<int:pk>/', PlanDetail.as_view()),
]

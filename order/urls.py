from django.urls import path, include
from order import views
from .views import checkout, MyOrdersView  

urlpatterns = [
    path('checkout/', views.checkout),
    path('orders/', MyOrdersView.as_view(), name="my-orders"),
    # path('orders/', views.OrdersList.as_view()),
]
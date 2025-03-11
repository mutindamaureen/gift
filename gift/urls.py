from django.urls import path, include
from gift import views
from .views import product_list, search_products, ProductDetail


urlpatterns = [
    path('products/', product_list, name='product_list'),
    # path('products/<int:pk>/', product_detail, name='product_detail'),

    # path('latest-products/', views.LatestProductsList.as_view(), name='latest-products'), 
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    # path('products/search', views.search),
    path('products/search', search_products, name='search_products'),
    # path('products/search/', ProductSearchView.as_view()),
]


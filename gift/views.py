from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import ProductSerializer
from PIL import Image
from io import BytesIO
from django.http import Http404
from rest_framework import status
from rest_framework import generics


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get(self, request, category_slug, product_slug):
        try:
            product = Product.objects.get(category__slug=category_slug, slug=product_slug)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def search_products(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(name__icontains=query)  
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response([], status=200)  


from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer
"""
This is added to show a list of all categories to  admin/staff users.
"""
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


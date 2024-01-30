from django.shortcuts import render
from rest_framework.views import APIView
from .models import ItemsModel
from .serializers import ItemsSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from django.http import Http404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
class DataList(APIView):
    
    def get(self, request, format=None):
        models = ItemsModel.objects.all()
        serializer = ItemsSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DataUpdateDelete(APIView):
   
    def get_object(self, pk):
        try:
            return ItemsModel.objects.get(pk=pk)
        except ItemsModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ItemsSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ItemsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ProductSearchAPIView(generics.ListAPIView):
    queryset = ItemsModel.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    
class AdminDashboard(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        content = {"message": "Welcome to the Admin Dashboard!"}
        return Response(content)

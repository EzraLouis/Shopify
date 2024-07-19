from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

class CustomerAPIView(APIView):
    def get(self, request):
        # Your logic here
        data = {"message": "Hello, this is the customer API!"}
        return Response(data)

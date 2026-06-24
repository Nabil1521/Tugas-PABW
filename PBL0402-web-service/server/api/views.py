from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Car
from .serializers import CarSerializer
from django.db.models import Q


@api_view(['GET'])
def index(request):
    """Simple index endpoint to check server status"""
    return Response({"message": "Server Ready"})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def car_list(request):
    """
    Handle CRUD operations for cars
    GET: List all cars
    POST: Create a new car
    PUT: Update a car by carname
    DELETE: Delete a car by carname
    """
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cars = Car.objects.all()
            all_cars = CarSerializer(cars, many=True)
            return Response(all_cars.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        carname = request.data.get('carname')
        if not carname:
            return Response(
                {"error": "carname is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            car = Car.objects.get(carname=carname)
        except Car.DoesNotExist:
            return Response(
                {"error": "Car not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cars = Car.objects.all()
            all_cars = CarSerializer(cars, many=True)
            return Response(all_cars.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        carname = request.data.get('carname')
        if not carname:
            return Response(
                {"error": "carname is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            car = Car.objects.get(carname=carname)
            car.delete()
        except Car.DoesNotExist:
            pass
        
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def read_data(request):
    """Legacy endpoint for reading all cars"""
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_cars(request, searchkey):
    """Search cars by name, brand, or model"""
    cars = Car.objects.filter(
        Q(carname__icontains=searchkey) |
        Q(carbrand__icontains=searchkey) |
        Q(carmodel__icontains=searchkey)
    )
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

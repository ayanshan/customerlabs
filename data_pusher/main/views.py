from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer

@api_view(['GET', 'POST'])
def account_list_create(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, account_id):
    account = get_object_or_404(Account, account_id=account_id)
    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Destination CRUD
@api_view(['GET', 'POST'])
def destination_list_create(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'GET':
        serializer = DestinationSerializer(destination)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DestinationSerializer(destination, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        destination.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Get destinations for an account
@api_view(['GET'])
def get_destinations_by_account(request, account_id):
    destinations = Destination.objects.filter(account__account_id=account_id)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

# Incoming data handler
@api_view(['POST'])
def incoming_data(request):
    secret_token = request.headers.get("CL-X-TOKEN")
    if not secret_token:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    account = Account.objects.filter(app_secret_token=secret_token).first()
    if not account:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    if not isinstance(data, dict):
        return Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    destinations = Destination.objects.filter(account=account)

    for destination in destinations:
        headers = destination.headers
        method = destination.http_method
        url = destination.url

        try:
            if method == 'GET':
                response = requests.get(url, params=data, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)

            print(f"Sent to {url} - Response: {response.status_code}")

        except requests.RequestException as e:
            print(f"Failed to send data to {url}: {e}")

    return Response({"message": "Data sent successfully"}, status=status.HTTP_200_OK)


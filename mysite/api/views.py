from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.serializers import Option_Serializer
from options.models import Option_Model

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ API VIEWS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@api_view(['GET', 'POST'])
def options(request):
    ''' create an option contract in the database'''
    if request.method == 'GET':
        options = Option_Model.objects.all()
        serializer = Option_Serializer(options, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = Option_Serializer(data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stock_option_list(request, ticker):
    """list of all option contracts with a given ticker"""
    if request.method == 'GET':
        ticker = ticker.replace('-', ' ').upper()
        options = Option_Model.objects.filter(stock_ticker = ticker)
        serializer = Option_Serializer(options, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def option_detail(request, ticker, pk):
    """Retrieve, update or delete option contracts."""
    try:
        option = Option_Model.objects.get(pk=pk)
    except Option_Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Option_Serializer(option)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Option_Serializer(option , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

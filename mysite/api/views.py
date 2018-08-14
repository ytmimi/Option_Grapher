from django.shortcuts import render
from options.models import Option_Model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ API VIEWS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@csrf_exempt
def option_list(request):
    """list of all option contracts"""
    if request.method == 'GET':
        options = Option_Model.objects.all()
        serializer = Option_Serializer(options, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Option_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

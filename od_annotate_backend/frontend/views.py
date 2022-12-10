from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from utils.semtab_views import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def semtab(request):
    data = {"success": False}
    
    if request.method == 'POST':
        if request.POST.get('file_link'):
            file_link = request.POST.get('file_link')
            #file_link = "small.csv"
            print("=========================================Begin processing")
            data = annotate_table(request, file_link)
            data["success"] = True
            print("=========================================End processing")

    return JsonResponse(data)

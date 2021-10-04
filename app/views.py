# from django.http import request
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
import json
# from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

# from django.views.generic import View


# NOTE:app/index.htmlが呼び出されるリターンされる。
def index(request):
    return HttpResponse('top')


# NOTE:'api/vl/boot'が呼び出されるとjsonを返す。クラス
class BootView(View):
    def get(self, request):
        data = {
            'test_massage': 'Is this right(Boot)'
        }
        return JsonResponse(data=data)


# NOTE:'api/vl/verify-pincode'が呼び出されるとjsonを返す。クラス
class Verify_pincode(View):
    def get(self, request):
        data = {
            'test_massage': 'Is this right(Verify_pincode)'
        }
        return JsonResponse(data=data)


# NOTE:'api/vl/prodict-image'が呼び出されるとjsonを返す。クラス
class Predict_image(View):
    def get(self, request):
        data = {
            'test_massage': 'Is this right(Prodict_image)'
        }
        return JsonResponse(data=data)

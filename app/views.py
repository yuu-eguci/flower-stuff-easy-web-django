# Built-in modules.
import os

# Third-party modules.

# User modules.
from app.utils import prediction_utils

# from django.http import request
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# NOTE:app/index.htmlが呼び出されるリターンされる。
def index(request):
    return HttpResponse('top')


class StatusView(View):
    def get(self, request):
        # 手元に hdf5 が存在することを ready=true と解釈します。
        data = dict(
            ready=os.path.exists(settings.APP_HDF5_PATH_IN_APP),
        )
        return JsonResponse(data=data)


@method_decorator(csrf_exempt, name='dispatch')
class VerifyPincodeView(View):
    def post(self, request):
        # 必須パラメータをチェックします。 pincode がなければ BadRequest です。
        if 'pincode' not in request.POST:
            return HttpResponseBadRequest('pincode is required.')

        # pincode をチェックします。
        data = dict(
            verification_succeeded=request.POST['pincode'] == settings.APP_PINCODE,
        )
        return JsonResponse(data=data)


@method_decorator(csrf_exempt, name='dispatch')
class PredictImageView(View):
    def post(self, request):
        # 必須パラメータをチェックします。必須パラメータがなければ BadRequest です。
        if 'base64image' not in request.POST:
            return HttpResponseBadRequest('base64image is required.')

        # Prediction を行います。
        prediction = prediction_utils.predict_base64image(request.POST['base64image'])

        # Prediction の結果を、 json 用に整形します。
        def for_json(tuple_: tuple) -> dict:
            # ('Sunflower', 0.9995204)
            # -> {'name':'Sunflower', 'confidence'=0.9995204} 変換します。
            name = tuple_[0]
            # json は float32 を serialize しません。 str にしてしまいます。
            confidence = str(tuple_[1])
            return dict(name=name, confidence=confidence)
        result = list(map(lambda tuple_: for_json(tuple_), prediction))

        data = dict(
            hdf5_version=settings.APP_HDF5_VERSION,
            result=result,
        )
        return JsonResponse(data=data)

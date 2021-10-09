# Built-in modules.
import os
import json

# Third-party modules.

# User modules.
from app.utils import common_utils
from app.utils import prediction_utils

# from django.http import request
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# このモジュール用のロガーを作成します。
logger = common_utils.get_my_logger(__name__)


# NOTE:app/index.htmlが呼び出されるリターンされる。
def index(request):
    return HttpResponse('top')


class StatusView(View):
    def get(self, request):
        print('StatusView.get from print')
        logger.debug('でばーぐ from logger')
        logger.info('いんーふぉ from logger')
        logger.warning('うぉーにん from logger')
        logger.error('えろあ from logger')
        logger.fatal('ふぇーたる(critical と同じっぽい) from logger')
        logger.critical('くりてぃこぉ from logger')
        try:
            # 手元に hdf5 が存在することを ready=true と解釈します。
            data = dict(
                ready=os.path.exists(settings.APP_HDF5_PATH_IN_APP),
            )
            return JsonResponse(data=data)
        except Exception:
            # 例外は raise されず、スタックトレースだけ残します。
            logger.exception('Something went wrong in StatusView.get')
            return HttpResponseServerError('Something went wrong.')


@method_decorator(csrf_exempt, name='dispatch')
class VerifyPincodeView(View):
    def post(self, request):
        try:
            # WARN: request.POST は json のやり取りには使えません。
            body_dict = json.loads(request.body)
            # 必須パラメータをチェックします。 pincode がなければ BadRequest です。
            if 'pincode' not in body_dict:
                return HttpResponseBadRequest('pincode is required.')

            # pincode をチェックします。
            data = dict(
                verification_succeeded=body_dict['pincode'] == settings.APP_PINCODE,
            )
            return JsonResponse(data=data)
        except Exception:
            # 例外は raise されず、スタックトレースだけ残します。
            logger.exception('Something went wrong in VerifyPincodeView.post')
            return HttpResponseServerError('Something went wrong.')


@method_decorator(csrf_exempt, name='dispatch')
class PredictImageView(View):
    def post(self, request):
        try:
            # WARN: request.POST は json のやり取りには使えません。
            body_dict = json.loads(request.body)
            # 必須パラメータをチェックします。必須パラメータがなければ BadRequest です。
            if 'base64image' not in body_dict:
                return HttpResponseBadRequest('base64image is required.')

            # Prediction を行います。
            prediction = prediction_utils.predict_base64image(body_dict['base64image'])

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
        except Exception:
            # 例外は raise されず、スタックトレースだけ残します。
            logger.exception('Something went wrong in PredictImageView.post')
            return HttpResponseServerError('Something went wrong.')

import requests
import jwt

from rest_framework import status
from django.views import View
from django.http import JsonResponse
from DRF_board.settings import *
from users.models import User


def get_kakao_user(access_token):
    kakao_url = 'https://kapi.kakao.com/v2/user/me'
    header = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(kakao_url, headers=header)

    if response.status_code == 200:
        return response.json()

    elif response.status_code == 401:
        return JsonResponse({'message': 'Authorization'}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return JsonResponse({'message': 'ResponseError'}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_access_token = request.headers['Authorization']
            user_info = get_kakao_user(kakao_access_token)

            kakao_id = user_info['id']
            email = user_info['kakao_account']['email']
            name = user_info['kakao_account']['profile']['nickname']

            user, is_created = User.objects.get_or_create(
                kakao_id=kakao_id,
                email=email,
                name=name,
            )
            print("user :", user.id)

            token = jwt.encode({"id": user.id}, os.environ['SECRET_KEY'], os.environ['ALGORITHM'])

            if is_created == False:
                return JsonResponse({"MESSAGE": "SUCCESS", "Authorization": token}, status=status.HTTP_200_OK)
            return JsonResponse({"MESSAGE": "CREATED", "Authorization": token}, status=status.HTTP_201_CREATED)

        except KeyError:
            return JsonResponse({"MESSAGE": "KeyError"}, status=status.HTTP_400_BAD_REQUEST)

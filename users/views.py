import requests, jwt, os
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from users.models import User
from dotenv import load_dotenv
load_dotenv()

'''
ACCESS_TOKEN = 
# 프론트단이 토큰 받아올때의 json 형태(이미 로그인한 상태의 토큰이 발급됨)
request = {
    "token_type":"bearer",
    "access_token":"${ACCESS_TOKEN}",
    "expires_in":43199,
    "refresh_token":"${REFRESH_TOKEN}",
    "refresh_token_expires_in":25184000,
    "scope":"account_email profile"
}
'''

# class KakaoUserAPI:
def get_kakao_user(access_token):
    kakao_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization' : f'Bearer {access_token}'}
    response = requests.get(kakao_url, headers = headers)

    if not response.status_code == 200:
        return Response({'message' : 'ResponseError'}, status=status.HTTP_400_BAD_REQUEST)
    return response.json()


# 파라미터 : 액세스 토큰을 헤더에 get, post로 담아서 넘기기
# 파라미터 : target_id,target_id_type, 사용자 회원번호 함께 전달(어드민키경우)
class KakaoLoginView(View):
    def post(self, request):
        try:
            '''
            받은 토큰 정보로 db에 유저 정보를 입력할것

            '''
            kakao_access_token = request.headers['Authorization']
            user_info = get_kakao_user(kakao_access_token)

            name = user_info['kakao_account']['profile']['nickname']
            phone_number = user_info['kakao_account']['phone_number']
            profile_image_url = user_info['kakao_account']['profile']['profile_image_url']
            kakao_id =  user_info['id']
            email = user_info['kakao_account']['email']
            
            if not User.objects.filter(email == email).exists():
                user, is_created = User.objects.get_or_create(
                name = name,
                phone_number = phone_number,
                profile_image_url = profile_image_url,
                kakao_id = kakao_id,
                email = email
            )
            
            token = jwt.encode({"id" : user.id}, os.environ['SECRET_KEY'], os.environ['ALGORITHM'])
            return Response({"token" : token}, status = status.HTTP_200_OK)

        except:
            return 
import json, jwt, os

from django.http import JsonResponse
from users.models import User
from board.models import Category, Post
from django.views import View

from dotenv import load_dotenv
load_dotenv()

class BoardView(View):
    #@login_decorator # 유저 여부 걸러짐
    def post(self, request):
        access_token = request.headers['Authorization']
        decode_token = jwt.decode(access_token, os.environ['SECRET_KEY'], os.environ['ALGORITHM'])
        request.user = User.objects.get(id=decode_token['id'])
        '''
        request = {
        kakao user 정보:
        title :
        content:
        category_id:
        }

        '''

        data = json.loads(request.body)
        title = data['title']
        content = data['content']
        user = data['user_id']
        category_id = data['category_id']

        Post.object.create(
            title = title,
            content = content,
            user = user.id,
            category = category_id
        )
        return JsonResponse({"message":"post create"}, status=201)
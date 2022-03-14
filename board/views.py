import json, os, jwt

from django.http import JsonResponse
from users.models import User
from board.models import Post, Category
from django.views import View

from dotenv import load_dotenv

load_dotenv()


class BoardView(View):
    # @login_decorator # 유저 여부 걸러짐
    def post(self, request):
        access_token = request.headers['Authorization']
        decode_token = jwt.decode(access_token, os.environ['SECRET_KEY'], os.environ['ALGORITHM'])
        request.user = User.objects.get(id=decode_token['id'])
        '''
        request = {
        kakao user 정보: reqeust.header
        title :
        content:
        category_id:
        }

        '''

        data = json.loads(request.body)
        category = Category.objects.get(id = data['category_id'])
        title = data['title']
        content = data['content']
        category_id = category

        print("5", title)
        print("6", content)
        print("5", category_id)
        print("7", request.user.id)

        Post.objects.create(
            title=title,
            content=content,
            user=request.user,
            category=category_id
        )
        return JsonResponse({"message": "post create"}, status=201)

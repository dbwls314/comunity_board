from django.db import models
from core.models import TimeStampModel

class User(TimeStampModel):
    name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    profile_image_url = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    kakao_id = models.IntegerField()
    email = models.CharField(max_length=250, unique=True)

    class Meta:
        db_table = 'users'

class Like(models.Model):
    isLiked = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('board.Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('board.Comment', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'likes'

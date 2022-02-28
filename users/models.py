from django.db import models
from core.models import TimeStampModel

class User(TimeStampModel):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    profile_image_url = models.ImageField(max_length=200)
    description = models.TextField()
    kakao_id = models.IntegerField()
    email = models.CharField(max_length=500)

    class Meta:
        db_table = 'users'

class Like(models.Model):
    isLiked = models.BooleanField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('board.Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('board.Comment', on_delete=models.CASCADE) 
    
    class Meta:
        db_table = 'likes'

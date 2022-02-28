from django.db import models
from users.models import User
from core.models import TimeStampModel

class Category(models.Model):
    category = models.CharField(max_length=100)
    main_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='Category')
    
    class Meta:
        db_table = 'categories'

class Post(TimeStampModel):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    read_count = models.ImageField()

    class Meta:
        db_table = 'posts'

class Comment(TimeStampModel):
    commnet = models.TextField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    main_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True )
    
    class Meta:
        db_table = 'comments'

class TagPost(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.RESTRICT)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag_posts'

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    posts = models.ManyToManyField('Post', through=TagPost)

    class Meta:
        db_table = 'tags'

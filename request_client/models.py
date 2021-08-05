from django.db import models


class SearchKeyword(models.Model):
    '''
    For saving search keywords and for giving search sugguestions
    '''
    keyword_id = models.AutoField(primary_key=True)
    keyword = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'search_keyword'


class PostComments(models.Model):
    '''
    For saving Post Comments 
    '''
    comment_id = models.AutoField(primary_key=True)
    fk_keyword = models.ForeignKey('SearchKeyword', on_delete=models.CASCADE, db_column='FK_keyword_id')  
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'post_comments'        
from django.db import models



# class SearchKeyword(models.Model):
#     keyword_id = models.AutoField(primary_key=True)
#     keyword  = models.CharField(max_length=255,unique=True)
    

#     class Meta:
#         managed=True
#         db_table = 'search_keyword'



# class PostComments(models.Model):
#     comment_id = models.AutoField(primary_key=True)
#     # FK_keyword_id = models.ForeignKey(SearchKeyword,on_delete=models.CASCADE)
#     FK_keyword_id = models.IntegerField()
#     comment   = models.TextField()

#     class Meta:
#         managed=True
#         db_table = 'post_comments'


class SearchKeyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    keyword = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'search_keyword'


class PostComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    fk_keyword = models.ForeignKey('SearchKeyword', on_delete=models.CASCADE, db_column='FK_keyword_id')  
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'post_comments'        
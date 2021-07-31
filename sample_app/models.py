from django.db import models



class SampleModel(models.Model):
    pk_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=50)
    phone_no = models.BigIntegerField(blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'sample_model'


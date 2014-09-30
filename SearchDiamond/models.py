from django.db import models

# Create your models here.


# class Diamonds(models.Model):
#     color = models.CharField(max_length=30)
#     cut = models.CharField(max_length=30)
#     polish = models.CharField(max_length=30)
#     symmetry = models.CharField(max_length=30)
#     fluorescence = models.CharField(max_length=30)
#     shape = models.CharField(max_length=30)
#     certification = models.CharField(max_length=30)
#     price = models.CharField(max_length=30)
#     purity = models.CharField(max_length=30)
#     weight = models.CharField(max_length=30)
#     certificationID = models.CharField(max_length=30)

class Diamonds(models.Model):
    color = models.CharField(max_length=30)
    cut = models.CharField(max_length=30)
    polish = models.CharField(max_length=30)
    sym = models.CharField(max_length=30)
    flo = models.CharField(max_length=30)
    shape = models.CharField(max_length=30)
    cert = models.CharField(max_length=30)
    price = models.FloatField(max_length=30)
    purity = models.CharField(max_length=30)
    weight = models.FloatField(max_length=30)
    zsh = models.CharField(max_length=30)
    
    def __unicode__(self):
        return '%s' % (self.shape)
from django.db import models

# Create your models here.
class ECGFiles(models.Model):
    file = models.FileField('ECGFiles', upload_to = 'ecg_files/')

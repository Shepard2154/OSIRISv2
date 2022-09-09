from django.db import models


class HFile(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    imageUrl = models.FileField(blank=True, null=True, upload_to='./backend/static/')
    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'files'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
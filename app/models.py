from django.db import models

# Create your models here.
# プロフィールモデルの作成。
class Profile(models.Model):
    title = models.CharField('タイトル', max_length=100, null=True, blank=True)
    name = models.CharField('名前', max_length=100)

    def __str__(self):
        return self.name

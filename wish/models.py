from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Wish(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', upload_to='wishcrafts/')
    caption = models.CharField('Подпись', max_length=350)
    link = models.URLField('Ссылка на картинку')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, related_name='wishcrafts', on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Желание'
        verbose_name_plural = 'Желания'

    def __str__(self):
        return f'{self.caption} - {self.user}'

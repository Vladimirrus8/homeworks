from django.db import models


class Sensor(models.Model):
    """
    Модель датчика температуры.
    """
    name = models.CharField(
        max_length=50,
        verbose_name='Название датчика'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} (ID: {self.id})'


class Measurement(models.Model):
    """
    Модель измерения температуры.
    """
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name='Датчик'
    )
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Температура'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время измерения'
    )
    image = models.ImageField(
        upload_to='measurements/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-created_at']

    def __str__(self):
        return f'Измерение датчика {self.sensor_id}: {self.temperature}°C'
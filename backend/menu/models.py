from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    url = models.CharField(max_length=255, help_text="URL or Named URL")

    def __str__(self):
        return self.title

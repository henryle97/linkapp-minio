import uuid

from django.db import models


# Create your models here.
class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.file.name

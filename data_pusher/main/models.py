from django.db import models
import uuid

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    app_secret_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    HTTP_METHOD_CHOICES = [('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="destinations")
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES)
    headers = models.JSONField()

    def __str__(self):
        return self.url


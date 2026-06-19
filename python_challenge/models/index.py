from django.db import models


class Index(models.Model):

    type = models.CharField(max_length=100)
    value = models.FloatField(blank=True, null=True)
    month = models.IntegerField()
    year = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "year", "month"], name="unique_index_type"),
        ]

from django.db import models


class Text(models.Model):
    name = models.CharField(unique=True, max_length=50, db_index=True)
    body = models.TextField()

    def __unicode__(self):
        return self.body

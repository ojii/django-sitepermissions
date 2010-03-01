from django.db import models


class SiteGroup(models.Model):
    group = models.ForeignKey('auth.Group', unique=True)
    sites = models.ManyToManyField('sites.Site')
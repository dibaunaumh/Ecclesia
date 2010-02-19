from django.db import models
from django.utils.translation import gettext_lazy as _

class Presentable(models.Model):
    x = models.IntegerField(default=0, verbose_name=_('x position'), help_text=_('Horizontal posinition in view from left border.'))
    y = models.IntegerField(default=0, verbose_name=_('y position'), help_text=_('Vertical posinition in view from top border.'))
    w = models.IntegerField(default=150, verbose_name=_('width'), help_text=_("Object's width."))
    h = models.IntegerField(default=100, verbose_name=_('height'), help_text=_("Object's height."))

    class Meta:
        abstract = True
from django.db import models
from django.utils.translation import gettext_lazy as _

class Presentable(models.Model):
    x_pos = models.IntegerField(default=0, help_text=_('Initial horizontal posinition in view from left border.'))
    y_pos = models.IntegerField(default=0, help_text=_('Initial vertical posinition in view from top border.'))
    width = models.IntegerField(default=150, help_text=_('Initial object width.'))
    height = models.IntegerField(default=100, help_text=_('Initial object height.'))

    class Meta:
        abstract = True
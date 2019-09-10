from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(AppConfig):
    icon = '<i class="large material-icons">phone_android</i>'
    name = 'app'
    verbose_name = _('Api_Management')
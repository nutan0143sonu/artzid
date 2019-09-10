from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class StaticContentConfig(AppConfig):
    icon = '<i class="large material-icons">home</i>'
    name = 'static_content'
    verbose_name = _('Static_Content')


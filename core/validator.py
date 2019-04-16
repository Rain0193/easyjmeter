from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_empty_str(value):
    if value == '':
        raise ValidationError(
            _('不能为空'),
            params={},
        )
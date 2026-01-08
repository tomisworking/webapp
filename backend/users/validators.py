import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    Walidator hasła wymagający:
    - Minimum 12 znaków
    - Przynajmniej jedna duża litera
    - Przynajmniej jedna mała litera
    - Przynajmniej jedna cyfra
    - Przynajmniej jeden znak specjalny
    """
    
    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError(
                _("Hasło musi zawierać minimum 12 znaków."),
                code='password_too_short',
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Hasło musi zawierać przynajmniej jedną dużą literę."),
                code='password_no_upper',
            )
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Hasło musi zawierać przynajmniej jedną małą literę."),
                code='password_no_lower',
            )
        
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Hasło musi zawierać przynajmniej jedną cyfrę."),
                code='password_no_digit',
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;\'`~]', password):
            raise ValidationError(
                _("Hasło musi zawierać przynajmniej jeden znak specjalny (!@#$%^&* itp.)."),
                code='password_no_special',
            )
    
    def get_help_text(self):
        return _(
            "Hasło musi zawierać minimum 12 znaków, w tym: "
            "dużą literę, małą literę, cyfrę i znak specjalny."
        )

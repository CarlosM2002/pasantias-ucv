from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils.translation import gettext_lazy as _


class SpanishMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length=min_length)
        self.message = _(
            "La contraseña es demasiado corta. Debe contener al menos %(min_length)d caracteres."
        )
        self.code = 'password_too_short'

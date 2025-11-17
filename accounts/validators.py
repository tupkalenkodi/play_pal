from django.core.exceptions import ValidationError
import re


class CustomComplexityValidator:
    def __init__(self, min_length):
        self.min_length = min_length

    def validate(self, password):
        # CHECK MINIMUM LENGTH
        if len(password) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long.",
                code='password_too_short',
            )

        # CHECK THAT AT LEAST ONE UPPERCASE LETTER IS PRESENT
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                f"Password must contain at least one uppercase letter.",
                code='password_no_upper',
            )

        # CHECK THAT AT LEAST ONE LOWERCASE LETTER IS PRESENT
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                f"Password must contain at least one lowercase letter.",
                code='password_no_lower',
            )

        # CHECK THAT AT LEAST ONE DIGIT LETTER IS PRESENT
        if not re.search(r'\d', password):
            raise ValidationError(
                f"Password must contain at least one digit.",
                code='password_no_digit',
            )

        # # CHECK THAT AT LEAST ONE SPECIAL CHAR IS PRESENT
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                f"Password must contain at least one special character.",
                code='password_no_special',
            )

    def get_help_text(self):
        return (f"Your password must contain at least {self.min_length} characters, "
                f"including one uppercase letter, one lowercase letter, one number, "
                f"and one special character.")

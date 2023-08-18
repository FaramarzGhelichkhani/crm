from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
import random
import string


def generate_password(length=6):
    chars = string.ascii_letters + string.digits  # + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


class CustomUserManager(BaseUserManager):
    """  
    Custom user model manager where phone is the unique identifiers  
    for authentication instead of usernames.  
    """

    def create_user(self, phone, password, **extra_fields):
        """  
        Create and save a User with the given phon number and password.  
        """
        if not phone:
            raise ValueError(('The phone must be set'))

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """  
        Create and save a SuperUser with the given phone and password.  
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)

    def get_full_name(self):
        '''  
        Returns the first_name plus the last_name, with a space in between.  
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class CustomPhoneNumberField(PhoneNumberField):
    def to_python(self, value):
        parsed_number = phonenumbers.parse(value, "IR")
        if parsed_number:
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        return None

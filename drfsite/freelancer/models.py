from django.db import models
import re
from rest_framework import serializers


class Position(models.TextChoices):
    BE_DEVELOPER = "Backend Developer"
    FE_DEVELOPER = "Frontend Developer"
    DEVOPS = "DevOps"

# id = models.AutoField(primary_key=True, blank=True)
#     name = models.CharField(max_length=255, blank=True, validators=[Validator.validate_name])
#     email = models.CharField(max_length=255, blank=True, validators=[Validator.validate_email])
#     phone_number = models.CharField(max_length=255, blank=True, validators=[Validator.validate_phone_number])
#     availability = models.CharField(max_length=255, blank=True, validators=[Validator.validate_availability])
#     salary = models.CharField(max_length=255, blank=True, validators=[Validator.validate_salary])
#     position = models.CharField(max_length=255, choices=Position.choices, validators=[Validator.validate_position])


class Validator:
    @staticmethod
    def validate_natural_number(some_string):
        if Validator.validate_int(some_string):
            return int(some_string) >= 0
        return False

    @staticmethod
    def validate_float(some_string):
        try:
            float(some_string)
            return True
        except Exception as exc:
            return False

    @staticmethod
    def validate_int(some_string):
        if Validator.validate_float(some_string):
            try:
                int(some_string)
                return True
            except Exception as exc:
                return False
        return False

    @staticmethod
    def validate_boundaries(number, lower_bound, upper_bound):
        return lower_bound <= number <= upper_bound

    @staticmethod
    def validate_string_with_letters_only(string_data):
        return all(letter.isalpha() for letter in string_data)

    @staticmethod
    def validate_capitalized(string_data):
        return string_data == string_data.capitalize()

    @staticmethod
    def validate_email(email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        if bool(re.match(email_pattern, email)):
            return True
        raise serializers.ValidationError(f"Is not Valid email")

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = r'^(\+?380\d{9}|380\d{9})$'
        if bool(re.match(pattern, phone_number)):
            return True
        raise serializers.ValidationError(f"Is not Valid phone number")

    @staticmethod
    def validate_salary(salary):
        if Validator.validate_float(salary):
            return True
        raise serializers.ValidationError(f"should be positive float")

    @staticmethod
    def validate_availability(availability):
        if Validator.validate_float(availability):
            if Validator.validate_boundaries(float(availability), 0, 72):
                return True
        raise serializers.ValidationError(f"should be float in range of 0 and 72")

    @staticmethod
    def validate_position(position):
        valid_choices = [choice[0] for choice in Position.choices]
        if position not in valid_choices:
            raise serializers.ValidationError(f"should be DevOps, Backend Developer or Frontend Developer")
        return True

    @staticmethod
    def validate_name(name):
        if Validator.validate_string_with_letters_only(name):
            return True
        raise serializers.ValidationError(f"should be capitalized string with only Letters")


class Freelancer(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    availability = models.FloatField()
    salary = models.FloatField()
    position = models.CharField(max_length=255, choices=Position.choices)

    def __str__(self):
        return self.id

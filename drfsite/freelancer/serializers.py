from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Freelancer, Validator
import re


class FreelancerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Freelancer
        # fields = ("id", "name", "email", "phone_number",
        #           "availability", "salary", "position")
        fields = "__all__"

    def validate_name(self, value):
        Validator.validate_name(value)
        return value

    def validate_email(self, value):
        Validator.validate_email(value)
        return value

    def validate_phone_number(self, value):
        Validator.validate_phone_number(value)
        return value

    def validate_availability(self, value):
        Validator.validate_availability(value)
        return value

    def validate_salary(self, value):
        Validator.validate_salary(value)
        return value

    def validate_position(self, value):
        Validator.validate_position(value)
        return value

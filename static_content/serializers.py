
from rest_framework import serializers

from static_content.models import *

class PrivacyPolicySerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"

class TermsAndConditionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = "__all__"

class AboutUsserializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        models = Careers
        fields = "__all__"
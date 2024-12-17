

from rest_framework import serializers
from . import models

class ProfileSerializer(serializers.ModelSerializer):
    user      = serializers.PrimaryKeyRelatedField(read_only = True)
    countries = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = models.Profile
        fields = [
                "user",
                "meta",
                "countries",
                "waiver",
                "last_mailed",
                "unsubscribed",
            ]

from rest_framework import serializers

from python_challenge.models.index import Index


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ['type', 'value', 'month', 'year']

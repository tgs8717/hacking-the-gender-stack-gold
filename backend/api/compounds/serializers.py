from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CharField
from api.models import Core
from api.models import CompoundRepo


class CompoundRequestSerializer(Serializer):
    smiles = CharField(required=True)


class CompoundModelSerializer(ModelSerializer):
    class Meta:
        model = CompoundRepo
        fields = "__all__"

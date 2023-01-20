from rest_framework.response import Response
from rest_framework.views import APIView

from api.compounds.serializers import CompoundRequestSerializer
from api.compounds.serializers import CompoundModelSerializer
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema

from api.core.examples import EXAMPLE_REQUEST


class Compounds(APIView):
    serializer_class = CompoundRequestSerializer

    def get(self, request):
        return Response(
            {
                "status": [1, 2, 3],
            }
        )

    @extend_schema(
        examples=[
            OpenApiExample(name="Example", value=EXAMPLE_REQUEST, request_only=True)
        ]
    )
    def post(self, request):
        serializer = CompoundRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # whatever processing you want to do goes here!

        # The output we are to return is saved in the database first
        modelSerializer = CompoundModelSerializer(
            data={"smiles": serializer.validated_data["smiles"], "logP": 86}
        )  # logP value here is made up!

        modelSerializer.is_valid(raise_exception=True)
        modelSerializer.save()

        return Response({"output": serializer.validated_data})

from rest_framework.response import Response

# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.compounds.serializers import CompoundRequestSerializer
from api.compounds.serializers import CompoundModelSerializer
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema

from api.core.examples import EXAMPLE_REQUEST

from api.models import CompoundRepo
from science.rdkit_endpoints import get_QED_props


class Compounds(ModelViewSet):
    serializer_class = CompoundRequestSerializer
    queryset = CompoundRepo.objects.all()

    # List all data we have in the database in shorthand
    def list(self, request):
        queryset = self.get_queryset()
        modelSerializer = CompoundModelSerializer(queryset, many=True)
        responseList = modelSerializer.data
        # for core in responseList:
        # core["rgroup_labels"] = core["rgroup_labels"].split(",")   #change this part if you want some processing done here
        return Response(modelSerializer.data)

    # Get a single stored entry by Id
    def retrieve(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response = serializer.data
        # response["rgroup_labels"] = response["rgroup_labels"].split(",")  #Process the data based on what gets returned and what you want to do
        return Response(response)

    @extend_schema(
        examples=[
            OpenApiExample(name="Example", value=EXAMPLE_REQUEST, request_only=True)
        ]
    )
    # Create a smiles entry, process it and store it in the database
    def create(self, request):
        serializer = CompoundRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # what should I do with the data here?
        smilesGiven = serializer.validated_data.get("smiles")
        raw = get_QED_props([smilesGiven])

        params = raw.get(smilesGiven)

        processed = {
            "smiles": smilesGiven,
            "MW": params.get("MW"),
            "ALOGP": params.get("ALOGP"),
            "HBA": params.get("HBA"),
            "HBD": params.get("HBD"),
            "PSA": params.get("PSA"),
            "ROTB": params.get("ROTB"),
            "AROM": params.get("AROM"),
            "ALERTS": params.get("ALERTS"),
            "WEIGHTED_QED": params.get("WEIGHTED_QED"),
        }

        print("PROCSSED VALUES")
        print(processed.get("ALOGP"))
        print(processed.get("WEIGHTED_QED"))

        # save the entry in the database
        modelSerializer = CompoundModelSerializer(data=processed)

        modelSerializer.is_valid(raise_exception=True)
        modelSerializer.save()

        # return Response({"output": serializer.validated_data})

        # see if you can
        # return the success message (but be sure to return something!)
        return Response({"status": "Entry created successfully"})

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from wineapi.models import Style

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['id', 'name']


class StyleViewSet(ViewSet):

    def list(self, request):
        styles = Style.objects.all()
        serializer = StyleSerializer(styles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            style = Style.objects.get(pk=pk)
            serializer = StyleSerializer(style)
            return Response(serializer.data, status=status.HTTP_200_OK )
        except Style.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
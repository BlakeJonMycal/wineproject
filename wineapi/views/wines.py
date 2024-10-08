from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import serializers
from wineapi.models import Wine, Style
from .styles import StyleSerializer


class WineSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    styles = StyleSerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user

    class Meta:
        model = Wine
        fields = ['id', 'name', 'region', 'vintage', 'abv', 'tasting_notes', 'grape_variety', 'vineyard', 'image_url', 'rating', 'is_owner', 'styles']


class WineViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        mine = request.query_params.get('mine', 'false').lower() == 'true'
        region = request.query_params.get('region', None)
        name = request.query_params.get('name', None)
        styles = request.query_params.getlist('styles', None)
        
        if mine:
            queryset = Wine.objects.filter(user=request.auth.user)
        else:
            queryset = Wine.objects.all()
        if region:
            queryset = queryset.filter(region__icontains=region)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if styles:
            queryset = queryset.filter(styles__in=styles).distinct()
            
        serializer = WineSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            wine = Wine.objects.get(pk=pk)
            serializer = WineSerializer(wine, context={'request': request})
            return Response(serializer.data)

        except Wine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        name = request.data.get('name')
        region = request.data.get('region')
        vintage = request.data.get('vintage')
        abv = request.data.get('abv')
        tasting_notes = request.data.get('tasting_notes')
        grape_variety = request.data.get('grape_variety')
        vineyard = request.data.get('vineyard')
        image_url = request.data.get('image_url')
        rating = request.data.get('rating')



        # Create a book database row first, so you have a
        # primary key to work with
        wine = Wine.objects.create(
            user=request.user,
            name=name,
            region=region,
            vintage=vintage,
            abv=abv,
            tasting_notes=tasting_notes,
            grape_variety=grape_variety,
            vineyard=vineyard,
            image_url=image_url,
            rating=rating)

        # Establish the many-to-many relationships
        style_ids = request.data.get('styles', [])
        wine.styles.set(style_ids)

        serializer = WineSerializer(wine, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            wine = Wine.objects.get(pk=pk)
            self.check_object_permissions(request, wine)

            style_ids = request.data.pop('styles', [])

            serializer = WineSerializer(wine, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
            # Update the wine instance with the validated data
                serializer.save()

            # Handle the styles field separately
                wine.styles.set(style_ids)

            # Return the updated wine data
                serializer = WineSerializer(wine, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Wine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):

        try:
            wine = Wine.objects.get(pk=pk)
            if wine.user.id == request.auth.user.id:
                wine.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You did not create this wine'}, status=status.HTTP_403_FORBIDDEN)

        except Wine.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
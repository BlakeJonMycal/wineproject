from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from wineapi.models import Wine
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

    def list(self, request):
        wines = Wine.objects.all()
        serializer = WineSerializer(wines, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get('title')
        author = request.data.get('author')
        isbn_number = request.data.get('isbn_number')
        cover_image = request.data.get('cover_image')

        # Create a book database row first, so you have a
        # primary key to work with
        book = Book.objects.create(
            user=request.user,
            title=title,
            author=author,
            cover_image=cover_image,
            isbn_number=isbn_number)

        # Establish the many-to-many relationships
        category_ids = request.data.get('categories', [])
        book.categories.set(category_ids)

        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:

            book = Book.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this book?
            self.check_object_permissions(request, book)

            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                book.title = serializer.validated_data['title']
                book.author = serializer.validated_data['author']
                book.isbn_number = serializer.validated_data['isbn_number']
                book.cover_image = serializer.validated_data['cover_image']
                book.save()

                category_ids = request.data.get('categories', [])
                book.categories.set(category_ids)

                serializer = BookSerializer(book, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            self.check_object_permissions(request, book)
            book.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
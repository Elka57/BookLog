from rest_framework import serializers

from users.api.serializers import UserSerializer
from journal.models import Author, Book, BookLog, Genre, Like, Quote, Share, BookTypes
# serializers.py

class AuthorSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True, allow_null=True, required=False)

    class Meta:
        model = Author
        fields = [
            'id',
            'first_name', 'last_name', 'patronymic',
            'birthday', 'death', 'country', 'photo',
            'status',                   # ← добавили
        ]
        read_only_fields = ['id', 'status']

class GenreSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Genre
    fields = ['id', 'title', 'description']
    read_only_fields = ['id']

class BookSerializer(serializers.ModelSerializer):
  logo = serializers.ImageField(use_url=True, allow_null=True, required=False)
  genre = GenreSerializer(read_only=True)
  type_text = serializers.SerializerMethodField()

  class Meta:
    model = Book
    fields = ['id', 'title', 'author', 'genre', 'logo', 'symbols', 'type_text', 'type']
    read_only_fields = ['id']

  def get_type_text(self, obj):
    return BookTypes(obj.type).label
  
class BookLogSerializer(serializers.ModelSerializer):
  book = BookSerializer(read_only=True)
  
  class Meta:
    model = BookLog
    fields = ['id', 'book', 'start', 'end', 'topic', 'score', 'three_sentences', 
              'new_knowledge', 'transformed_me', 'impressions', 'ideas', 'heroes', 
              'begin', 'key_events', 'most_important_event', 'result', 'created_at', 
              'updated_at']
    read_only_fields = ['id']


class LikeSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  quote = serializers.PrimaryKeyRelatedField(read_only=True)
  
  class Meta:
    model = Like
    fields = ['id', 'user', 'quote', 'moment']
    read_only_fields = ['id']


class ShareSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  quote = serializers.PrimaryKeyRelatedField(read_only=True)
  
  class Meta:
    model = Share
    fields = ['id', 'user', 'quote', 'moment', 'destination']
    read_only_fields = ['id']


class QuoteSerializer(serializers.ModelSerializer):
  book = BookSerializer(read_only=True)
  book_log = BookLogSerializer(read_only=True)

  likes  = LikeSerializer(source='like_records',  many=True, read_only=True)
  shared = ShareSerializer(source='share_records', many=True, read_only=True)


  class Meta:
    model = Quote
    fields = ['id', 'book', 'note', 'likes', 'shared', 'privat', 'book_log']
    read_only_fields = ['id']


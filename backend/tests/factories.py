# tests/factories.py

import factory
from factory import Faker
from factory.django import DjangoModelFactory

from users.models import User, UserTypes
from journal.models import (
    Author, Genre, Book, BookLog, Quote, Like, Share,
    ApprovalStatus, BookTypes,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "pass1234")
    user_type = UserTypes.READER.value   # <-- теперь строка/число, как ожидает модель


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    patronymic = Faker("first_name")               # можно заменить на None
    birthday = Faker("date_of_birth")
    death = None
    country = Faker("country")
    photo = None
    status = ApprovalStatus.APPROVED
    biography = Faker("paragraph")
    created_by = factory.SubFactory(UserFactory)


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    title = Faker("sentence", nb_words=3)
    description = Faker("text")
    status = ApprovalStatus.APPROVED
    created_by = factory.SubFactory(UserFactory)


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = Faker("sentence", nb_words=3)
    author = factory.SubFactory(AuthorFactory)
    genre = factory.SubFactory(GenreFactory)
    logo = None
    symbols = Faker("random_int", min=10000, max=500000)
    type = BookTypes.FICTION
    status = ApprovalStatus.APPROVED
    created_by = factory.SubFactory(UserFactory)


class BookLogFactory(DjangoModelFactory):
    class Meta:
        model = BookLog

    book = factory.SubFactory(BookFactory)
    start = Faker("date")
    end = Faker("date")
    topic = Faker("sentence")
    score = Faker("random_int", min=1, max=10)
    three_sentences = Faker("paragraph", nb_sentences=3)
    new_knowledge = Faker("sentence")
    transformed_me = Faker("sentence")
    impressions = Faker("sentence")
    ideas = Faker("sentence")
    heroes = Faker("name")
    begin = Faker("sentence")
    key_events = Faker("sentence")
    most_important_event = Faker("sentence")
    result = Faker("sentence")


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    note = Faker("sentence")
    book = factory.SubFactory(BookFactory)
    book_log = factory.SubFactory(BookLogFactory)
    privat = False


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like
        django_get_or_create = ("user", "quote")

    user = factory.SubFactory(UserFactory)
    quote = factory.SubFactory(QuoteFactory)


class ShareFactory(DjangoModelFactory):
    class Meta:
        model = Share

    user = factory.SubFactory(UserFactory)
    quote = factory.SubFactory(QuoteFactory)
    destination = Faker("url")

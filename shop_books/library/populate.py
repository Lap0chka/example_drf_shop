from django.contrib.auth.models import User
from faker import Faker
from rest_framework.generics import get_object_or_404

from library.models import Author, Book, Category, Comment
import random

fake = Faker()

def create_authors(n):
    for _ in range(n):
        author = Author(
            name=fake.first_name(),
            surname=fake.last_name(),
            city=fake.city(),
            born=random.randint(1800, 2000),
            died=random.randint(1900, 2023) if random.choice([True, False]) else None,
            country=fake.country()
        )
        author.save()

def create_books(n):
    authors = Author.objects.all()
    for _ in range(n):
        book = Book(
            title=fake.sentence(nb_words=3),
            description=fake.text(),
            page=random.randint(100, 1000),
            publication_date=fake.date()
        )
        book.save()
        book.author.set(random.sample(list(authors), random.randint(1, 3)))
        book.save()

def create_category(n):
    for _ in range(n):
        category = Category(
            name=fake.word(),
        )
        category.save()


def create_comments(n):
    for _ in range(n):
        comment = Comment(
            book = get_object_or_404(Book, id=random.randint(1, 25)),
            user = get_object_or_404(User, id=1),
            text = fake.text(),
        )
        comment.save()


create_comments(30)


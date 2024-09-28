from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from typing import Optional, List

User = get_user_model()

class Author(models.Model):
    """Represents an author of books."""
    name: str = models.CharField(max_length=50, db_index=True)
    surname: str = models.CharField(max_length=50, db_index=True)
    slug: str = models.SlugField(unique=True)
    biography: Optional[str] = models.TextField(null=True, blank=True)
    city: Optional[str] = models.CharField(max_length=50, null=True, blank=True)
    born: Optional[int] = models.IntegerField(null=True, blank=True)
    died: Optional[int] = models.IntegerField(default=None, null=True, blank=True)
    country: Optional[str] = models.CharField(max_length=50, null=True, blank=True)
    image: Optional[models.ImageField] = models.ImageField(upload_to='author/', null=True, blank=True)
    book: List['Book'] = models.ManyToManyField('Book', blank=True, related_name='written_by_authors')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['surname', 'name']),
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Automatically create slug from name and surname if not provided."""
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.surname}')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'


class Category(models.Model):
    """Represents a category for books."""

    name: str = models.CharField(max_length=50, db_index=True)
    slug: str = models.SlugField(unique=True)
    parent: Optional['Category'] = models.ForeignKey('self', null=True, blank=True,
                                                     on_delete=models.CASCADE, related_name='children')

    class Meta:
        unique_together = (['slug', 'parent'])
        indexes = [
            models.Index(fields=['name']),
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Automatically create slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """Represents a book with its attributes."""

    title: str = models.CharField(max_length=100, db_index=True)
    slug: str = models.SlugField(unique=True)
    description: str = models.TextField()
    author: List[Author] = models.ManyToManyField(Author, related_name='written_books')
    page: int = models.IntegerField()
    publication_date: Optional[models.DateField] = models.DateField(null=True, blank=True)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    publisher: Optional[str] = models.CharField(max_length=100, null=True, blank=True)
    image: Optional[models.ImageField] = models.ImageField(upload_to='books/', null=True, blank=True)
    category: List[Category] = models.ManyToManyField(Category, related_name='books')

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        """Automatically create slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Represents a comment on a book."""

    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    text: Optional[str] = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    parent: Optional['Comment'] = models.ForeignKey('self', null=True, blank=True,
                                                    on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_at']

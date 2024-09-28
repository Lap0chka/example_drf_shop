from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(unique=True)
    biography = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    born = models.IntegerField(null=True, blank=True)
    died = models.IntegerField(default=None, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='author/', null=True, blank=True)
    book = models.ManyToManyField('Book', blank=True, related_name='written_by_authors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['surname', 'name']),
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.surname}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')

    class Meta:
        unique_together = (['slug', 'parent'])
        indexes = [
            models.Index(fields=['name']),
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class Book(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    author = models.ManyToManyField(Author, related_name='written_books')
    page = models.IntegerField()
    publication_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='books')

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        ordering = ['title', ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}')
        super().save(*args, **kwargs)




class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_at']
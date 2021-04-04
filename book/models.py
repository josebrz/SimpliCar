from django.db import models


class Library(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=100)
    author = models.ForeignKey('book.Author', on_delete=models.CASCADE)
    libraries = models.ManyToManyField('book.Library')

    def __str__(self):
        return self.title


class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lead(models.Model):

    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    library = models.ForeignKey('book.Library', on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.fullname, self.email)
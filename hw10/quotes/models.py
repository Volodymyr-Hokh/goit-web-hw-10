from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.fullname
    

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()

    def __str__(self) -> str:
        return self.quote

from django.db import models


class Geo(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    geo = models.ForeignKey(Geo, on_delete=models.CASCADE)

    def __str__(self):
        return self.street


class Profile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    active = models.BooleanField()
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="listings")
    image = models.CharField(max_length=128, blank=True, null=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="winning_list")
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="wins")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f"{self.user} {self.amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} {self.listing}"


    

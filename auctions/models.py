from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category 

class Listing(models.Model):
    item_name = models.CharField(max_length=64) 
    description = models.CharField(max_length=500, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    starting_bid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings") 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_owned")
    date_created = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}. {self.item_name} -- ({self.category})" 

class Bid(models.Model):
    auction_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="items")
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidders")
    bid_amount = models.IntegerField()
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction_id.item_name} -- bidded by ({self.bidder_id.username})" 

class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.CharField(max_length=100)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


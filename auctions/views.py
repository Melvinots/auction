from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Category, Listing, Bid, Comment


def index(request, category=None):

    # Get all active listings
    lists = Listing.objects.filter(closed=False).order_by("-date_created")

    # Attempt to filter listings by category
    if category:
        category_obj = Category.objects.get(category=category)
        lists = lists.filter(category=category_obj)

    return render(request, "auctions/index.html", {
        "category": category,
        "lists": lists
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required
def create(request):
    if request.method == "POST":
        item_name = request.POST["item_name"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        owner = request.POST["owner"]

        # Creates a new listing
        listing = Listing(
            item_name=item_name, 
            description=description, 
            image_url=image_url, 
            starting_bid=starting_bid, 
            category=Category.objects.get(category=category), 
            owner=User.objects.get(username=owner)
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })


def listings(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    contents = Comment.objects.filter(auction=listing).order_by("-comment_time")

    if request.method == "POST":

        # Close auction 
        listing.closed = True
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
    # Display page of a specific item
    else:
        
        # Determine if item is already in user's watchlist
        listed = False
        try:
            if listing in request.user.watchlist.all():
                listed = True
        except AttributeError:
            pass

        # Determine proper messages to be displayed
        bid_obj = Bid.objects.filter(auction_id=listing)
        num_bid =  len(bid_obj)
        highest_bid = bid_obj.order_by("-bid_amount").first()

        if highest_bid and highest_bid.bidder_id.id == request.user.id:
            num_bid_message = f"{num_bid} bid(s) so far. Your bid is the current highest bid."
        else:
            num_bid_message = f"{num_bid} bid(s) so far."

        if highest_bid and highest_bid.bidder_id.id == request.user.id and listing.closed:
            win_message = "Congratulations! You've won the auction!"
        elif listing.closed:
            win_message = "This auction is closed."
        else:
            win_message = "Auction is still ongoing!"

        return render(request, "auctions/listing.html", {
            "listed": listed,
            "listing": listing,
            "current_bid": highest_bid,
            "num_bid": num_bid_message,
            "contents": contents,
            "win_message": win_message
        })


@login_required
def watchlists(request, listing_id=None):
    user = request.user
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)

        # add/remove item from user's watchlist
        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlists": user.watchlist.all()
        })


@login_required
def category_view(request):
    categories = Category.objects.all().order_by("category")
    return render(request, "auctions/category.html", {
        "categories": categories
    })


@login_required
def bid_view(request, listing_id):
    if request.method == "POST":
        bid_amount = int(request.POST["bid_amount"])
        listing = Listing.objects.get(pk=listing_id)

        # Get the highest bid for the item
        highest_bid = Bid.objects.filter(auction_id=listing_id).order_by("-bid_amount").first()
        
        # Check if user has already placed a bid
        bidding = Bid.objects.filter(auction_id=listing_id, bidder_id=request.user).first()

        if bidding:
            if bid_amount > highest_bid.bid_amount:
                bidding.bid_amount = bid_amount
                bidding.save()
                messages.info(request, "Your bid was successfully updated.")
            else:
                messages.warning(request, "Your bid must be higher than the current bid.")
        else:
            if bid_amount >= listing.starting_bid and (not highest_bid or bid_amount > highest_bid.bid_amount):
                bid = Bid(auction_id=listing, bidder_id=request.user, bid_amount=bid_amount)
                bid.save()
                messages.info(request, "Your bid was successfully placed.")
            elif not highest_bid:
                messages.warning(request, "Your bid must be equal or higher than the current price.")
            else:
                messages.warning(request, "Your bid must be higher than the current bid.")
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))
    
    else:
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))
    

@login_required
def comment_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id) 
    if request.method == "POST":
        content = request.POST["content"]
        comment = Comment(auction=listing, commenter=request.user, content=content)
        comment.save()
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))
    return HttpResponseRedirect(reverse("listings", args=[listing_id]))

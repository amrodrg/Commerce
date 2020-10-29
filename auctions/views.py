from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from auctions.models import Listing, User, Comment, Bid, Category


def index(request):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


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


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        sbid = request.POST["bid"]
        category_title = request.POST["category"]
        categories = []
        for c in Category.objects.all():
            categories.append(c.title)
        if category_title not in categories:
            category = Category(title=category_title)
            category.save()
        category = Category.objects.get(title=category_title)
        image = request.POST["image"]
        listing = Listing(active=True, creater=request.user, title=title,description=description,starting_bid=sbid,category=category,image=image)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")


def listing_page(request, ID):
    watchlist = request.session["watchlist"]
    if request.method == "POST":
        if ID in watchlist:
            wl = request.session["watchlist"]
            wl.remove(ID)
            request.session["watchlist"] = wl
            return render(request, "auctions/listing_page.html", {
            "listing": Listing.objects.get(pk=ID),
            "button": "add to watchlist",
            "min_bid": Listing.objects.get(pk=ID).starting_bid+1,
            "comments": Listing.objects.get(pk=ID).comments.all()
            })
        else:
            request.session["watchlist"] += [ID]
            return render(request, "auctions/listing_page.html", {
            "listing": Listing.objects.get(pk=ID),
            "button": "remove from watchlist",
            "min_bid": Listing.objects.get(pk=ID).starting_bid+1,
            "comments": Listing.objects.get(pk=ID).comments.all()
            })

    else: 
        if ID in watchlist:
            return render(request, "auctions/listing_page.html", {
            "listing": Listing.objects.get(pk=ID),
            "button": "remove from watchlist",
            "min_bid": Listing.objects.get(pk=ID).starting_bid+1,
            "comments": Listing.objects.get(pk=ID).comments.all()
            })
        else:
            return render(request, "auctions/listing_page.html", {
            "listing": Listing.objects.get(pk=ID),
            "button": "add to watchlist",
            "min_bid": Listing.objects.get(pk=ID).starting_bid+1,
            "comments": Listing.objects.get(pk=ID).comments.all()
            })

def bid(request, ID):
    if request.method == "POST":
        newBid = request.POST["newBid"]
        print(newBid)
        l = Listing.objects.get(pk=ID)
        l.starting_bid = newBid
        l.highest_bidder = request.user
        l.save()
        BID = Bid(user=request.user, amount=newBid )
        BID.save()
        return HttpResponseRedirect(reverse("listing", args=(ID,)))

    return HttpResponseRedirect(reverse("listing", args=(ID,)))

def comment(request, ID):
    if request.method == "POST":
        comment_text = request.POST["comment"]
        comment = Comment(user=request.user, listing=Listing.objects.get(pk=ID), text=comment_text)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(ID,)))

def watchlist_view(request):
    watchlist = request.session["watchlist"]
    listings = []
    for ID in watchlist:
        listings.append(Listing.objects.get(pk=ID))
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def categories_list(request):
    return render(request, "auctions/categories_list.html", {
        "categories": Category.objects.all()
    })

def category_view(request, ID):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=ID).listings.all(),
        "category_title": Category.objects.get(pk=ID).title
    })

def close(request, ID):
    if request.method == "POST":
        l = Listing.objects.get(pk=ID)
        l.active = False
        l.winner = l.highest_bidder
        l.save()
        return HttpResponseRedirect(reverse("index"))


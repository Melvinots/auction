# Auction Django Project

## Introduction

Welcome to the Auction Django Project! This project is a web application that allows users to create, view, and bid on auction listings. It features user authentication, real-time bidding, and a simple & clean, responsive UI to enhance the user experience.

## Features

- User Authentication (Registration, Login, Logout)
- Create, View, and Manage Auction Listings
- Real-Time Bidding
- Add/Remove Items from Watchlist
- Comment on Listings

## Usage

- **Home Page:** View all active auction listings.
- **Create Listing:** Click on the "Create Listing" button to add a new auction item.
- **Watchlist:** Add items to your watchlist to keep track of them.
- **Bid:** Place a bid on an auction item.
- **Comments:** Add comments to auction listings.
- **Manage Listings:** Users can close their own listings or remove items from their watchlist.

## Directory Structure

auction-django-project/<br>
├── auctions/<br>
│   ├── migrations/<br>
│   ├── static/<br>
│   │   └── auctions/<br>
│   │       └── images/<br>
│   ├── templates/<br>
│   │   └── auctions/<br>
│   ├── __init__.py<br>
│   ├── admin.py<br>
│   ├── apps.py<br>
│   ├── models.py<br>
│   ├── tests.py<br>
│   ├── urls.py<br>
│   ├── views.py<br>
├── commerce/<br>
│   ├── __init__.py<br>
│   ├── asgi.py<br>
│   ├── settings.py<br>
│   ├── urls.py<br>
│   ├── wsgi.py<br>
├── manage.py<br>
├── requirements.txt<br>

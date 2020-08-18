# Manual
## Installation
Before you can use SteamFGG you need to install it's dependencies.

#### Windows:
Execute the install.bat file.

#### Linux:
Type the following into your terminal:
> pip3 install -r requirements.txt

## Usage:
You can start SteamFGG from terminal by navigating to its directory
and typing:

#### Windows:
> python steam_fgg.py

Alternatively you can use the Batch file (steam_fgg.bat).
#### Linux:
> python3 steam_fgg.py


## Using your wishlist:
SteamFGG can use your Steam wishlist to find out if games are 
currently free.
##### Note: Your wishlist has to be public for this to work!

#### Setup:
In order for this to work you have to edit the configuration file (config.json)
like:
>"steam_profile_id": "your_profile_id",
>"use_wishlist": true

## Using the watchlist:
In case you don't want to use your wishlist you can create a watchlist by
editing the configuration file (config.json). 

#### Setup:
You just need to add the games shop page URL to the list ("watchlist") like:
>"watchlist": ["https://store.steampowered.com/app/220/HalfLife_2/",
>               "https://store.steampowered.com/app/240/CounterStrike_Source/"]

## Adding newsfeed sources:
You can add additional newsfeed sources by editing the config.json
file.
Keep in mind that sources must have the following base URL:
> https://store.steampowered.com/news/posts/?headlines=1

You can then add feeds by using the 'feed' GET parameter like:
> https://store.steampowered.com/news/posts/?headlines=1&feed=steam_community_announcements

## Optional SYS Args:
Argument | Alternative | Description
--- | --- | ---
-f  |--fast |  don't resolve game names

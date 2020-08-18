import os
import platform

STEAM_APP_URL = "http://store.steampowered.com/app/"    # TODO implement everywhere
WISHLIST_EP = "https://store.steampowered.com/wishlist/profiles/{}/wishlistdata/?p=0"
APPDETAIL_EP = "http://store.steampowered.com/api/appdetails/"

OS = platform.system()

if OS == "Windows":
    SEPARATOR = "\\"
elif OS == "Linux":
    SEPARATOR = "/"

APPDIR = os.path.dirname(os.path.realpath(__file__)) + SEPARATOR

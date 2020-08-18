import gevent.monkey
gevent.monkey.patch_all()   # needed to avoid max recursion error

from steam.client import SteamClient
from steam.client import EResult
import json
import argparse

from scraper.news_scraper import NewsScraper
from scraper.game_scraper import GameScraper
from scraper.topseller_scraper import TopsellerScraper
import api.public_api as pub_api
import constants as const


def request_free_game(client, appid_list):
    res = client.request_free_license(appid_list)
    return res


def create_steam_session():
    client = SteamClient()
    client.cli_login()
    return client


def analyse_newsfeeds(news_scraper, newsfeeds):
    local_appids = []

    print("\tanalysing:", news_scraper.url)  # analyse the first feed
    post_ids = news_scraper.extract_post_ids()
    local_appids += news_scraper.extract_appids(post_ids)

    for feed in newsfeeds:  # analyse the left feeds
        news_scraper.change_url(feed)
        print("\tanalysing:", news_scraper.url)

        post_ids = news_scraper.extract_post_ids()
        local_appids += news_scraper.extract_appids(post_ids)

    return local_appids


def analyse_game_pages(game_scraper, urls):
    local_appids = []

    appid = game_scraper.get_appid()
    if appid:
        local_appids.append(appid)

    for game_url in urls:
        game_scraper.change_url(game_url)

        appid = game_scraper.get_appid()
        if appid:
            local_appids.append(appid)

    return local_appids


if __name__ == "__main__":
    dump_path = const.APPDIR + "requested.json"
    config = json.load(open(const.APPDIR + "config.json"))
    appids = []
    wishlist_urls = None

    watchlist_used = len(config["watchlist"]) > 0
    wishlist_used = config["steam_profile_id"] != "" and config["use_wishlist"]

    argp = argparse.ArgumentParser(description="""SteamFGG is a small tool that scans Steam (newsfeed, wishlist, etc.) 
                                                    for currently free games and claims them for you 
                                                    if you tell it to do so.""")
    argp.add_argument("-f", "--fast", required=False,
                      help="don't resolve game names", action="store_true")
    args = vars(argp.parse_args())

    print("SteamFGG")
    print("Please wait this might take some time.")

    # INIT SCRAPERS
    print("initialising scrapers...")
    news_scraper = NewsScraper(config["newsfeeds"][0], config["filter_terms"])
    topseller_scraper = TopsellerScraper("https://store.steampowered.com/specials#p=0&tab=TopSellers")

    if watchlist_used:
        watchlist_scraper = GameScraper(config["watchlist"][0])

    if wishlist_used:
        wishlist_urls = pub_api.get_wishlist(config["steam_profile_id"])
        wishlist_scraper = GameScraper(wishlist_urls[0])

    # READ DUMP FILE
    try:
        requested = json.load(open(dump_path, "r"))     # used to not list games are already claimed
    except json.decoder.JSONDecodeError:
        requested = {"req": []}

    # ANALYSE NEWSFEED
    print("analysing newsfeed...")
    appids += analyse_newsfeeds(news_scraper, config["newsfeeds"][1:])

    # ANALYSE TOPSELLERS
    print("analysing topsellers...")
    topseller_urls = topseller_scraper.get_urls()
    topseller_game_scraper = GameScraper(topseller_urls[0])     # TODO somehow init with other scrapers
    appids += analyse_game_pages(topseller_game_scraper, topseller_urls[1:])

    # ANALYSE WATCHLIST
    if watchlist_used:
        print("analysing watchlist...")
        appids += analyse_game_pages(watchlist_scraper, config["watchlist"][1:])

    # ANALYSE WISHLIST
    if wishlist_used:
        print("analysing wishlist...")
        appids += analyse_game_pages(wishlist_scraper, wishlist_urls[1:])

    # FILTERING
    appids = list(filter(lambda a: a not in requested["req"], appids))  # filter already requested games
    appids = set(appids)    # remove duplicates

    # SHOW RESULTS
    if len(appids) > 0:
        print("I found following potentially free games:")
        for appid in appids:
            if args["fast"]:
                data = appid
            else:
                data = pub_api.appid_to_name(appid)
            print("\t-", data)

        # CLAIM GAMES
        if input("Do you want to claim this games? (y)") in ["Y", "y", "yes"]:
            session = create_steam_session()

            res = request_free_game(session, appids)

            if res[0] == EResult.OK:
                print("Claim request SUCCESSFUL")
            else:
                print("Claim request FAILED")
                print(res)

            requested["req"] += appids

        json.dump(requested, open(dump_path, "w"))
    else:
        print("I found no new free games")
    print("Good Bye")

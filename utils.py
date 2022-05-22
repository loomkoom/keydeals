import requests

applist_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
applist_json = requests.get(applist_url).json()

removed_url = 'https://steam-tracker.com/api?action=GetAppListV3'
removed_json = requests.get(removed_url).json()


def find_appid(game):
    appid = None
    for app in applist_json['applist']['apps']:
        title = app['name'].lower()
        if title == game.lower():
            appid = app['appid']
            # print(f"{appid:10}\t{title}")

    for app in removed_json['applist']['apps']:
        title = app['name'].lower()
        if title == game.lower():
            appid = app['appid']
            # print(f"{appid:10}\t{title}")

    if appid is None:
        print(f"NONE FOUND \t{game}")
        return None
    return appid


def find_title(id):
    title = None
    for app in applist_json['applist']['apps']:
        appid = app['appid']
        if appid == id:
            title = app['name']
            # print(f"{appid:10}\t{title}")

    if title is None:
        for app in removed_json['removed_apps']:
            appid = app['appid']
            if appid == id:
                title = app['name']
                # print(f"{appid:10}\t{title}")
    if title is None:
        print(f"NONE FOUND \t{id}")
        return None
    return title

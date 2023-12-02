import requests

apikey = "A708E43221865D149C791F9F4B57488A"

class SteamPowered:
    @staticmethod
    def get_player_summaries(steamids: list[str], format: str = "json"):
        params = dict(
            steamids=",".join(steamids),
            format=format,
            key=apikey
        )
        return requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=params).json()
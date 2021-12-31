from huokanadvertiserclient.core.discord.OAuthServer import OAuthServer


class DiscordOAuthListener:
    def __init__(self) -> None:
        server = OAuthServer(12345)

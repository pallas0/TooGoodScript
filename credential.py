class Credential:
    def __init__(self, access_token=None, refresh_token=None, user_id=None, cookie=None, subscriber_id=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.cookie = cookie
        self.subscriber_id = subscriber_id

    
import requests

class Remanga:
    def __init__(self):
        self.api = "https://api.remanga.org"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
        self.user_id = None
        self.access_token = None


    def generate_captcha(
            self,
            payload: str = "v=PRMRaAwB3KlylGQR57Dyk-pF&reason=q&c=<token>&k=6LdGNc8UAAAAAOi7mZdoujfQ0s-zHexDM8AWyB1J&co=aHR0cHM6Ly9uZXh0LnJlbWFuZ2Eub3JnOjQ0Mw..&hl=en&size=invisible&chr=%5B88%2C91%2C94%5D&vh=171805507&bg=!u72gvbgKAAQeG9ujbQEHDwNQThjPgVnP7bQGfGtLFTSQ9q7PRWq4Mo6wTK1hF6mTmob321ueoFddZBgl3CNxklbmAd_8x8YxYDs5QrjL7dUsYncpMGmkgC7zGhUD0BwVc3v8cz2Bpap3IHwTDlUSNRYp9EyzZ3WTmkn72WjZixVOb5MJrD7nfwq2T8c8XaIINt60LWpEgRbduOLUxBAynNNCbWdx4R_dhxK7wkXMFMv34aAr9Q8Kj7BGQqoXIU4Ipj_fUd_cuXF4AdbcCERBSRyELilo5WyMkx3yZA_SdwkCg1Dq9JvAHKlhw5nSl49hjcLvBdppQxiX40G_7-wW8f1yOHrBCCut2YB7fGS6TzqRroQhmwufQeuleX1aWRIX-gmXhVdv2-NscuqGbMCugcxXC6GIJK_E3I4fkr5TT6_J4KnmjJLIB23LVrax3N2Da7QXpEq6PhA1WGLrCKxdzONe46StOcc-tKK_zlbg2UCLm0GPV_Ai1qmKKipyCErtZIE4nuqUxbHddY6DUQ_a7tWEA_yDT5Y9txb5XdsdtpLPOULrzElUGyHDKD51acbNfw6sUk5c33LZl20XMJc9sTFSitCX_B1lTMyR63g6FMeZGcFshiVb8-kFdwSlphiiJRTc4hruXo-PtQKM1ZnU0mL2HfQ8D20qDrQIkRI2mMs8QV6vX0zhbCFQ4r6HMdKQQgvlPdox3JjwmXMdVX1jV_wx3JWObthRfEXocF39Km-hQYC-TP06Biej705zlTtXVQ5v5sMgDzBAfYP0sDUr9cjYplzKZ6rkxpCc3BOF1K2Tkfy4JN1mm5l9RpcayJHQyOlCBH_DsTbxqdTESD8uwSGZeTn7uEytRv3-AHA98Qr-gexjL1kEu4ZJBwFHfNIZTP2HSz8Wadvvtc-8pzkn74xljxgvhlbzl9tgshMv5mqicfwSv6rxKy0VWKLk66PwSRsNQM1y77SLQ3c3b73tpv7-c9MgyinRnc-SuxKOdPJLVUiXxd4hhcz7g1fyLSh_LaskcEMTWPKm_uAKHUPy1d7UerHiUc31CdFQaEi6X-knv_d2wVeQtYQhb0WKwfVPNLtbRhbZeMSFtzJWVpwvLq3pyWBvBcVxfvhmCLFAyRcalZLhcRoqXeLorrrwq6mBqBKcAEaCJSJCY7wmqzJbvhTimQGmw1GsPo5rfTeXVfEyJ8TBFTVcAETA_Cl6ea0QWEErqn22tv5EXs7tLRdbYr0jIX3ObDYfJoEq*"):
        anchor = requests.get(
            "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdGNc8UAAAAAOi7mZdoujfQ0s-zHexDM8AWyB1J&co=aHR0cHM6Ly9uZXh0LnJlbWFuZ2Eub3JnOjQ0Mw..&hl=ru&v=PRMRaAwB3KlylGQR57Dyk-pF&size=invisible&cb=x8tfd89z6xpn",
            headers=self.headers).text
        recaptcha_token = anchor.split('recaptcha-token" value="')[1].split('">')[0]
        data = payload.replace("<token>", recaptcha_token)
        response = requests.post(
            "https://www.google.com/recaptcha/api2/reload?k=6LdGNc8UAAAAAOi7mZdoujfQ0s-zHexDM8AWyB1J",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}).text
        if "rresp" in response:
            return response.split('"rresp","')[1].split('"')[0]

    def login(self, username: str, password: str):
        data = {
            "user": username,
            "password": password,
            "g-recaptcha-response": self.generate_captcha()
        }
        response = requests.post(
            f"{self.api}/api/users/login/",
            json=data,
            headers=self.headers).json()
        if "content" in response:
            self.access_token = response["content"]["access_token"]
            self.user_id = response["content"]["id"]
            self.headers["authorization"] = f"bearer {self.access_token}"
        return response

    def send_comment(
            self,
            text: str,
            title_id: int,
            is_pinned: bool = False,
            is_spoiler: bool = False):
        data = {
            "is_pinned": is_pinned,
            "is_spoiler": is_spoiler,
            "text": text,
            "title": title_id}
        return requests.post(
            f"{self.api}/api/activity/comments/?title_id={title_id}",
            json=data,
            headers=self.headers).json()

    def logging(self, path_name: str = "/"):
        data = {
            "user": self.user_id,
            "access_token": self.access_token,
            "msg": "CONSOLE",
            "location": {
                "pathname": path_name,
                "search": "",
                "hash": "",
                "key": ""},
            "deviceType": "desktop",
            "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
        return requests.post(
            f"{self.api}/api/logging/",
            json=data,
            headers=self.headers).json()

    def similar_titles(self, title: str):
        return requests.get(
            f"{self.api}/api/titles/{title}/similar/",
            headers=self.headers).json()

    def search_title(self, title: str, count: int = 5):
        return requests.get(
            f"{self.api}/api/search/?query={title}&count={count}",
            headers=self.headers).json()

    def search_publishers(self, username: str, page: int = 1, count: int = 10):
        return requests.get(
            f"{self.api}/api/search/?count={count}&field=publishers&page={page}&query={username}",
            headers=self.headers).json()

    def edit_profile(
            self,
            username: str = None,
            adult: bool = False,
            sex: int = 0,
            yaoi: int = 0):
        data = {"adult": adult, "sex": sex, "username": username, "yaoi": yaoi}
        return requests.put(
            f"{self.api}/api/users/current/",
            json=data,
            headers=self.headers).json()

    def get_report_reasons():
        return requests.get(
            f"{self.api}/api/reports/?get=reasons&type=title",
            headers=self.headers).json()

    def send_report(
            self,
            message: str,
            reason: int,
            title_id: int,
            type: str = "title"):
        data = {
            "message": message,
            "reason": reason,
            "target": title_id,
            "type": type}
        return requests.post(
            f"{self.api}/panel/api/reports/",
            json=data,
            headers=self.headers).json()

    def like_comment(self, comment_id: int, type: int = 0):
        data = {"comment": comment_id, "type": type}
        return requests.post(
            f"{self.api}/api/activity/votes/",
            json=data,
            headers=self.headers).json()


    def get_genres(self):
        return requests.get(
            f"{self.api}/api/forms/titles/?get=genres",
            headers=self.headers).json()

    def get_title_info(self, title: str):
        return requests.get(
            f"{self.api}/api/titles/{title}/",
            headers=self.headers).json()

    def get_title_chapters(self, branch_id: int):
        return requests.get(
            f"{self.api}/api/titles/chapters/?branch_id={branch_id}",
            headers=self.headers).json()

    def get_title_comments(self, title_id: int, page: int = 1):
        data = {"title_id": title_id, "page": page, "ordering": "-id"}
        return requests.get(
            f"{self.api}/api/activity/comments/?title_id={title_id}&page={page}&ordering=-id",
            json=data,
            headers=self.headers).json()

    def get_user_info(self, user_id: str):
        return requests.get(
            f"{self.api}/api/users/{user_id}",
            headers=self.headers).json()

    def get_notifications(self, count: int = 30, page: int = 1):
        return requests.get(
            f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=0",
            headers=self.headers).json()

    def get_notifications_count(self):
        return requests.get(
            f"{self.api}/api/users/notifications/count/",
            headers=self.headers).json()

    def get_account_info(self):
        return requests.get(
            f"{self.api}/api/users/current/",
            headers=self.headers).json()

    def get_daily_top_titles(self, count: int = 5):
        return requests.get(
            f"{self.api}/api/titles/daily-top/?count={count}",
            headers=self.headers).json()

    def get_titles_last_chapters(self, page: int = 1, count: int = 5):
        return requests.get(
            f"{self.api}/api/titles/last-chapters/?page={page}&count={count}",
            headers=self.headers).json()

    # bookmark types, 0 - reading, 1 - will read, 2 - readed, 3 - abandoned, 4 - postponed, 5 - not interesting
    def add_to_bookmarks(self, title_id: int, type: int):
        data = {"mangaId": title_id, "title": title_id, "type": type}
        return requests.post(
            f"{self.api}/api/users/bookmarks/",
            json=data,
            headers=self.headers).json()

    def change_password(self, old_password: str, new_password: str):
        data = {
            "old_password": old_password,
            "confirm_password": new_password,
            "password": new_password
        }
        return requests.put(
            f"{self.api}/api/users/current/",
            json=data,
            headers=self.headers).json()

    def bill_promo_code(self, promo_code: str):
        data = {
            "promo_code": promo_code
        }
        return requests.post(
            f"{self.api}/api/billing/promo-codes/",
            json=data,
            headers=self.headers).json()

    def create_publishers(self, name: str, vk_url: str):
        data = {"name": name, "vk": vk_url}
        return requests.post(
            f"{self.api}/api/publishers/",
            json=data,
            headers=self.headers).json()

    def rate_title(self, title_id: int, rating: int = 10):
        data = {"rating": rating, "title": title_id}
        return requests.post(
            f"{self.api}/api/activity/ratings/",
            json=data,
            headers=self.headers).json()

    def like_chapter(self, chapter_id: int, type: int = 0):
        data = {"chapter": chapter_id, "type": type}
        return requests.post(
            f"{self.api}/api/activity/votes/",
            json=data,
            headers=self.headers).json()

    def get_categories(self):
        return requests.get(
            f"{self.api}/api/forms/titles/?get=categories",
            headers=self.headers).json()

    def get_age_limits(self):
        return requests.get(
            f"{self.api}/api/forms/titles/?get=age_limit",
            headers=self.headers).json()

    def get_types(self):
        return requests.get(
            f"{self.api}/api/forms/titles/?get=types",
            headers=self.headers).json()

    def get_statuses(self):
        return requests.get(
            f"{self.api}/api/forms/titles/?get=status",
            headers=self.headers).json()

    def get_user_bookmarks(self, type: int, user_id: int, page: int = 1):
        return requests.get(
            f"{self.api}/api/users/{user_id}/bookmarks/?ordering=-chapter_date&page={page}&type={type}",
            headers=self.headers).json()

    def get_user_history(self, user_id: int, page: int = 1):
        return requests.get(
            f"{self.api}/api/users/{user_id}/history/?page={page}",
            headers=self.headers).json()

    def get_social_notifications(self, count: int = 30, page: int = 1):
        return requests.get(
            f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=1",
            headers=self.headers).json()

    def get_important_notifications(self, count: int = 30, page: int = 1):
        return requests.get(
            f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=2",
            headers=self.headers).json()

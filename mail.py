import requests

class MailTM():
    def __init__(self, username:str, password:str, address:str=None) -> None:
        self.username = username
        self.password = password
        self.created = False
        self.address = address

    def create(self):
        self.address = f"{self.username}@{self._domain()}"
        payload = {
            "address": self.address,
            "password": self.password
        }
        r = requests.post("https://api.mail.tm/accounts", json=payload, headers={"Content-Type": "application/json"})

        try:
            data = r.json()
            return data["address"]
        except:
            return False

    def checkMailbox(self):
        token = self._token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        r = requests.get("https://api.mail.tm/messages?page=1", headers=headers)

        return r.json()

    def _token(self):
        if self.address == None:
            raise Exception("Account not created")
        
        payload = {
            "address": self.address,
            "password": self.password
        }

        r = requests.post("https://api.mail.tm/token", json=payload, headers={"Content-Type": "application/json"})
        data = r.json()

        return data["token"]

    def _domain(self):
        r = requests.get("https://api.mail.tm/domains?page=1")
        data = r.json()
        return data["hydra:member"][0]["domain"]


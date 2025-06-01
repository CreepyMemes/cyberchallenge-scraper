import requests

class Session:
    """
    Session class that authenticates and stores in tokens for requests to the API
    """
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.token_auth = {}
        self.token_download = ""
        self.group = ""

        self._login(email, password)
    

    def _login(self, email: str, password: str):
        """
        Authenticates and stores session token and file download token.
        """
        resp = self.session.post(f"{self.base_url}/api/login", json={"email": email, "password": password})
        resp .raise_for_status()
        data = resp.json()

        token = data.get("token")
        files_token = data.get("filesToken")

        self.token_auth = {"authorization": f"Token {token}"}
        self.token_download = f"=&auth={files_token}"

        user_info = self.api_get("currentUser")
        self.group = user_info.get('group')


    def api_get(self, path: str) -> dict:
        """
        Performs an authenticated GET request to the API and returns the JSON response.
        """
        resp = self.session.get(f"{self.base_url}/api/{path}", headers=self.token_auth)
        resp.raise_for_status()

        return resp.json()


    def download_file(self, file_url: str, file_path: str):
        """
        Downloads a single file with the download token.
        """
        if not file_url.lower().startswith('/api/file'):
            return

        with open(file_path, 'wb') as f:
            resp = self.session.get(f"{self.base_url}{file_url}{self.token_download}")
            f.write(resp.content)


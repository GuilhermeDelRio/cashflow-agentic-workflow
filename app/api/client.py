import requests
from typing import Any, List
from app.api.exceptions import APIError
from app.config.settings import settings


class CashflowAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            try:
                error_data = e.response.json()
                raise APIError(
                    status_code=e.response.status_code,
                    message=error_data.get("message", str(e)),
                )
            except ValueError:
                raise APIError(status_code=e.response.status_code, message=str(e))
        except requests.RequestException as e:
            raise APIError(status_code=0, message=f"Connection failed: {e}")

    def create_expense(self, data: dict) -> dict:
        return self._request("POST", "/expenses/", json=data)

    def list_expenses(self) -> List[dict]:
        return self._request("GET", "/expenses/")

    def get_expense(self, expense_id: int) -> dict:
        return self._request("GET", f"/expenses/{expense_id}")

    def update_expense(self, expense_id: int, data: dict) -> dict:
        return self._request("PATCH", f"/expenses/{expense_id}", json=data)

    def delete_expense(self, expense_id: int) -> dict:
        return self._request("DELETE", f"/expenses/{expense_id}")


api_client = CashflowAPIClient(base_url=settings.cashflow_api_url)

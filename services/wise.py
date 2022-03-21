import json
import uuid
import requests

from fastapi import HTTPException, status

from core.config import settings


class WiseService:
    def __init__(self) -> None:
        self.main_url = settings.WISE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.WISE_TOKEN}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = self.main_url + "/v1/profiles"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response = response.json()
            return [element["id"] for element in response if element["type"] == "personal"][0]

        print(response)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def create_quote(self, amount):
        url = self.main_url + "/v2/quotes"
        body = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "profile": self.profile_id
        }
        response = requests.post(
            url, headers=self.headers, data=json.dumps(body))

        if response.status_code == 200:
            response = response.json()
            return response["id"]

        print(response)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def create_recipient_account(self, fullname, iban):
        url = self.main_url + "/v1/accounts"

        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": fullname,
            "legalType": "PRIVATE",
            "details":
                {
                    "iban": iban,
                }
        }

        response = requests.post(
            url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            response = response.json()
            return response["id"]

        print(response)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def create_transfer(self, target_account_id, quote_id):
        url = self.main_url + "/v1/transfers"
        customer_transaction_id = str(uuid.uuid4())

        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            response = response.json()
            return response["id"]

        print(response)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def fund_transfer(self, transfer_id):
        url = self.main_url + \
            f"/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"

        data = {
            "type": "BALANCE"
        }
        
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 201:
            response = response.json()
            return response

        print(response)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def cancel_funds(self, transfer_id):
        url = self.main_url + f"/v1//transfers/{transfer_id}/cancel"

        response = requests.put(url, headers=self.headers)

        if response.status_code == 200:
            response = response.json()
            return response["id"]

        print(response)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

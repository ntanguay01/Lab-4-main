# Nicholas Tanguay
# CSCI-2910 Server-Side Web Programming
# Lab 4

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.restcountries.com/countries/v5"


class ApiError(Exception):
    """Raised when a request fails. The message is safe to show the user."""


def _get(path="", params=None):
    # Send GET request to get info
    if not API_KEY:
        raise ApiError("No API key found. Add API_KEY=... to your .env file.")

    try:
        response = requests.get(
            f"{BASE_URL}{path}",
            params=params,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
    except requests.exceptions.RequestException as err:
        raise ApiError(f"Network problem: {err}") from err

    # The rate limit (20 requests / 10 seconds) is enforced before the API,
    # so a 429 has no JSON body.
    if response.status_code == 429:
        raise ApiError("Too many requests. Wait a few seconds and try again.")

    try:
        body = response.json()
    except ValueError as err:
        raise ApiError(f"Unexpected response (HTTP {response.status_code}).") from err

    if not response.ok:
        errors = body.get("errors", [])
        message = errors[0].get("message", "Unknown error") if errors else "Unknown error"
        raise ApiError(f"HTTP {response.status_code}: {message}")

    return body["data"]["objects"]


# Get country by name
def get_country_by_name(name):
    """Find countries whose name matches `name`.

    GET /countries/v5/name?q=japan
    Returns a list. It can hold several countries (e.g. "united").
    """
    return _get("/name", {"q": name})
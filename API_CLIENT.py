# Nicholas Tanguay
# CSCI-2910 Server-Side Web Programming
# Lab 4

import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.restcountries.com/countries/v5"
PAGE_SIZE = 100


class ApiError(Exception):
    """Raised when a request fails. The message is safe to show the user."""


def _request(path="", params=None):
    # Send GET request to get data
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
 
    return body["data"]
 
 
def _get(path="", params=None):
    # Return only the list of results form a single request
    return _request(path, params)["objects"]
 
 
def _get_all_pages(path="", params=None):
    params = dict(params or {})
    params["limit"] = PAGE_SIZE
    offset = 0
    results = []
 
    while True:
        params["offset"] = offset
        data = _request(path, params)
        results.extend(data["objects"])
        if not data["meta"].get("more"):
            return results
        offset += PAGE_SIZE


# Get country by name
def get_country_by_name(name):
    # Find country by name
   
    return _get("/name", {"q": name})

# Get country by code
def get_country_by_code(code):
    # Find country by three letter code 

    return _get(
        f"/codes.alpha_3/{code}",
        {"response_fields": "names.common,codes.alpha_3"},
    )

# Get countries by region
def get_countries_by_region(region):
    # Gets every country in user inputted region
    return _get_all_pages(
        f"/region/{region}",
        {"response_fields": "names.common,capitals,population"},
    )

# Get countries by currency
def get_countries_by_currency(currency_code):
    # Get every country from inputted currency
    return _get_all_pages(
        f"/currencies/{quote(currency_code)}",
        {"response_fields": "names.common,currencies"},
    )

# Get countries by spoken language
def get_countries_by_language(language):
    # Gets every country where inputted langauge is spoken
    fields = {"response_fields": "names.common,languages"}
    results = _get_all_pages(f"/languages/{quote(language)}", fields)
    if not results:
        results = _get_all_pages("/languages", {**fields, "q": language})
    return results
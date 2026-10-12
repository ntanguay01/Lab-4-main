# Nicholas Tanguay
# CSCI-2910 Server-Side Web Programming
# Lab 4

import random

from API_CLIENT import ApiError, get_country_by_name, get_country_by_code, get_countries_by_region, get_countries_by_currency, get_countries_by_language, get_all_countries

REGIONS = ["Africa", "Americas", "Asia", "Europe", "Oceania"]

# Menu
def print_menu():
    print("\n=== Country Explorer ===")
    print("1. Look up a country")
    print("2. Browse countries by region")
    print("3. Search by currency or language")
    print("4. Flag quiz")
    print("5. Exit")

# Choose Country from menu
def choose_country(matches):
    # If a search found several countries, let the user pick one.
    if len(matches) == 1:
        return matches[0]

    print(f"\nFound {len(matches)} matches:")
    for number, country in enumerate(matches, start=1):
        print(f"  {number}. {country['names']['common']}")

    while True:
        choice = input("Pick a number (or press Enter to cancel): ").strip()
        if choice == "":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(matches):
            return matches[int(choice) - 1]
        print("Please enter a number from the list.")

# Show country informtaion from user input
def show_country(country):
    names = country["names"]
    capitals = [c["name"] for c in country.get("capitals", [])]
    languages = [lang["name"] for lang in country.get("languages", [])]
    currencies = [f"{cur['name']} ({cur['symbol']})" for cur in country.get("currencies", [])]

    print(f"\n{country['flag']['emoji']}  {names['common']}")
    print(f"  Official name: {names['official']}")
    print(f"  Capital:       {', '.join(capitals) or 'N/A'}")
    print(f"  Population:    {country['population']:,}")
    print(f"  Languages:     {', '.join(languages) or 'N/A'}")
    print(f"  Currencies:    {', '.join(currencies) or 'N/A'}")
    print(f"  Flag image:    {country['flag']['url_png']}")

# Find neighboring countries from user inputted countries 
def show_neighbors(country):
    
    border_codes = country.get("borders", [])
 
    if not border_codes:
        print(f"\n{country['names']['common']} has no land borders.")
        return
 
    names = []
    for code in border_codes:
        try:
            matches = get_country_by_code(code) 
        except ApiError as err:
            print(f"\nCould not look up neighbor {code}: {err}")
            return
        # Fall back to the raw code if the API returns nothing for it
        names.append(matches[0]["names"]["common"] if matches else code)
 
    print(f"\nNeighbors of {country['names']['common']}: {', '.join(names)}")

# Look up country and give provided information
def lookup_country():
    name = input("\nCountry name: ").strip()
    if not name:
        print("Please type a country name.")
        return
 
    try:
        matches = get_country_by_name(name)
    except ApiError as err:
        print(f"\nCould not look up that country: {err}")
        return
 
    if not matches:
        print(f"\nNo countries found matching '{name}'.")
        return
 
    country = choose_country(matches)
    if country:
        show_country(country)
        if country.get("borders"):
            answer = input("\nShow neighboring countries? (y/n): ").strip().lower()
            if answer == "y":
                show_neighbors(country)

def browse_region():
    print("\nRegions:")
    for number, region in enumerate(REGIONS, start=1):
        print(f"  {number}. {region}")
 
    choice = input("Pick a region (or press Enter to cancel): ").strip()
    if choice == "":
        return
    if not (choice.isdigit() and 1 <= int(choice) <= len(REGIONS)):
        print("Please enter a number from the list.")
        return
    region = REGIONS[int(choice) - 1]
 
    try:
        countries = get_countries_by_region(region)
    except ApiError as err:
        print(f"\nCould not load {region}: {err}")
        return
 
    if not countries:
        print(f"\nNo countries found for {region}.")
        return
 
    countries.sort(key=lambda c: c.get("population", 0), reverse=True)
 
    show_all = False
    if len(countries) > 10:
        answer = input(f"\n{len(countries)} countries found. Show all? (y = all, Enter = top 10): ")
        show_all = answer.strip().lower() == "y"
    shown = countries if show_all else countries[:10]
 
    print(f"\n{region} - by population")
    print(f"  {'#':<4}{'Country':<32}{'Capital':<24}{'Population':>14}")
    for rank, country in enumerate(shown, start=1):
        capitals = [c["name"] for c in country.get("capitals", [])]
        print(
            f"  {rank:<4}{country['names']['common'][:30]:<32}"
            f"{(', '.join(capitals) or 'N/A')[:22]:<24}"
            f"{country.get('population', 0):>14,}"
        )

# Find country by currency used
def search_by_currency():
    code = input("\nCurrency code (e.g. EUR, USD, JPY): ").strip()
    if not code:
        print("Please enter a currency code.")
        return
 
    try:
        countries = get_countries_by_currency(code)
    except ApiError as err:
        print(f"\nCould not search by currency: {err}")
        return
 
    if not countries:
        print(f"\nNo countries found using the currency '{code.upper()}'.")
        return
 
    countries.sort(key=lambda c: c["names"]["common"])
    print(f"\n{len(countries)} countries use {code.upper()}:")
    for country in countries:
        # Show the matching currency's name and symbol
        match = next(
            (cur for cur in country.get("currencies", []) if cur["code"].lower() == code.lower()),
            None,
        )
        detail = f"{match['name']} ({match['symbol']})" if match else ""
        print(f"  {country['names']['common']:<34}{detail}")

# Find country by langauage spoken
def search_by_language():
    language = input("\nLanguage name in English (e.g. Spanish, French): ").strip()
    if not language:
        print("Please enter a language.")
        return
 
    try:
        countries = get_countries_by_language(language)
    except ApiError as err:
        print(f"\nCould not search by language: {err}")
        return
 
    if not countries:
        print(f"\nNo countries found where '{language}' is spoken.")
        return
 
    countries.sort(key=lambda c: c["names"]["common"])
    print(f"\n{len(countries)} countries where {language.title()} is spoken:")
    for country in countries:
        others = [
            lang["name"]
            for lang in country.get("languages", [])
            if lang["name"].lower() != language.lower()
        ]
        extra = f"Country also speaks: {', '.join(others)}" if others else ""
        print(f"  {country['names']['common']:<34}{extra}")

def search_menu():
    print("\nSearch by:")
    print("  1. Currency")
    print("  2. Language")
    choice = input("Pick an option (or press Enter to cancel): ").strip()
    if choice == "1":
        search_by_currency()
    elif choice == "2":
        search_by_language()
    elif choice != "":
        print("Please enter 1 or 2.")

 # Create flag quiz
def flag_quiz():
    print("\nLoading countries...")
    try:
        countries = get_all_countries()
    except ApiError as err:
        print(f"\nCould not load the quiz: {err}")
        return

    pool = [c for c in countries if c.get("classification", {}).get("sovereign")] or countries
    pool = [c for c in pool if c.get("flag", {}).get("emoji")]
    if not pool:
        print("No flag data available.")
        return
 
    rounds = input(f"How many rounds? (1-{len(pool)}, Enter = 5): ").strip()
    rounds = int(rounds) if rounds.isdigit() and 1 <= int(rounds) <= len(pool) else 5
 
    print("\nName the country! Type 'q' to quit early.")
    score = 0
    played = 0
 
    for number, country in enumerate(random.sample(pool, rounds), start=1):
        answer = country["names"]["common"]
        print(f"\nRound {number}/{rounds}:  {country['flag']['emoji']}")
        print(f"  (if you only see letters, open the image: {country['flag']['url_png']})")
        guess = input("Which country is this? ").strip()
 
        if guess.lower() == "q":
            break
        played += 1
        if guess.lower() == answer.lower():
            score += 1
            print("Correct!")
        else:
            print(f"Not quite. It was {answer}.")
 
    print(f"\nFinal score: {score}/{played}")

 # Print menu
def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            lookup_country()
        elif choice == "2":
            browse_region()
        elif choice == "3":
            search_menu()
        elif choice == "4":
            flag_quiz()
        elif choice == "5":
            print("Thank for playing!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main() 
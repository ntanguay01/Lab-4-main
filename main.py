# Nicholas Tanguay
# CSCI-2910 Server-Side Web Programming
# Lab 4

from API_CLIENT import ApiError, get_country_by_name, get_country_by_code 

# Menu
def print_menu():
    print("\n=== Country Explorer ===")
    print("1. Look up a country")
    print("2. Exit")

# Choose Country from menu
def choose_country(matches):
    """If a search found several countries, let the user pick one."""
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


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            lookup_country()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main() 
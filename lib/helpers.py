#! lib/helpers.py
from models.country import Country
from models.waterfall import Waterfall


def list_countries():
    countries = Country.get_all()
    print("Countries")
    print("******************************")
    for i, country in enumerate(countries, start = 1):
        print(f'{i}. {country.name}')
    print("******************************")

def get_country(index):
    countries = Country.get_all()
    country = countries[index - 1]
    
    print(f"waterfalls in {country.name}")
    print("*******************************")
    waterfalls = country.waterfalls()
    for i, waterfall in enumerate(waterfalls, start = 1): 
        print(f'{i}. {waterfall.name}')    
    print("*******************************")       
    
    country_waterfall_menu(country) 
            


def country_waterfall_menu(country):
    from cli import country_menu
    print("Please select the number of the waterfall to see its details ")
    txt = "or"
    o = txt.center(20)
    print(o)
    print("Press A or a to add a new waterfall to the country ")
    print("Press U or u to update country")
    print("Press D or d to delete the country ")
    print("Press B or b to go back to the previous menu ")
    print("Press E or e to exit program ")
    choice = input("> ")
    if choice.isdigit(): 
        number = int(choice)
        print(f"Information selected on waterfall in {country.name} ")
        print("*******************************")
        waterfall = country.waterfalls()[number - 1]
        print(f'Name: {waterfall.name} ')
        print(f'Location: {waterfall.location}')
        print(f'Elevation: {waterfall.elevation} ft') 
        print("*******************************")
        waterfall_menu(country, waterfall)
    if choice == "B" or choice == "b":
        country_menu()
    elif choice == "D" or choice == "d":
        delete_country(country)
        country_menu()
    elif choice == "U" or choice == "u":
        update_country()
        country_menu()
    elif choice == "A" or choice == "a":
        create_waterfall(country)
        get_country(country.id)
    elif choice == "E" or choice == "e":
        exit_program()
    else:
        print("Invalid Choice")

def waterfall_menu(country, waterfall):
    print("Press U or u to update waterfall")
    print("Press D or d to delete waterfall")
    print("Press B or b to go back to the previous menu")
    print("Press E or e to exit program")
    choice = input("> ")
    if choice == "U" or choice == "u":
        update_waterfall()
        get_country(country.id)

    elif choice == "D" or choice == "d":
        delete_waterfall(waterfall)
        get_country(country.id)
    elif choice == "B" or choice == "b":
        get_country(country.id)

    elif choice == "E" or choice == "e":
        exit_program()
    else:
        print("Invalid Choice")
                            

def choice_menu():
    from cli import main, country_menu
    print("Please select a number of the country to see more details")
    print("or")
    print("Press A or a to add new country")
    print("Press B or b to go back to the previous menu")
    print("Press E or e to exit program")
    choice = input("> ")
    if choice.isdigit():
        get_country(int(choice))
    elif choice == "a" or choice == "A":
        create_country()
        country_menu()
    elif choice == "b" or choice == "B":
        main()
    elif choice == "e" or choice == "E":
        exit_program()
    

def create_country():
    print("Add new country:")
    name = input("> ")
    try:
        country = Country.create(name)
        print(f' {country.name} created!')
    except Exception as exc:
        print(f"Error creating {country.name}", exc)
    

def update_country():
    name = input("Enter name of country: ")
    if country := Country.find_by_name(name):
        try:
            name = input("Enter a new country: ")
            country.name = name
            country.update()
            print(f'{country.name} updated!')
        except Exception as exc:
            print(f"Error updating {country.name} ", exc)
    else:
        print(f'Country {country.name} not found')

def delete_country(country):
    if country := Country.find_by_id(country.id):
       country.delete()
       print(f"{country.name} has been deleted!")
    else:
        print(f"Error deleting: {country.name} not found")

    

def create_waterfall(country):
    #entering input to create waterfall
    name = input("Enter name of waterfall: ")
    location = input("Enter town near waterfall: ")
    elevation = int(input("Enter the elevation of the waterfall: "))
    country_id = country.id

    try:
        waterfall = Waterfall.create(name, location, elevation, country_id)
        print(f' {waterfall.name} has been created')
    except Exception as exc:
        print(f"Error creating {waterfall.name}", exc)

def update_waterfall():
    from models.country import Country
    #updating name property of waterfall
    print("Enter name to change or press enter to keep:")
    name = input("> ")
    if waterfall:= Waterfall.find_by_name(name):
        try:
            print("Enter new name for waterfall: ")
            name = input("> ")
            waterfall.name = name
            waterfall.update()
        except Exception as exc:
            print("Error updating name", exc)
    #updating location property of waterfall
        print("Enter Town to change or press enter to keep: ")       
        location = input("> ")
        if waterfall:= Waterfall.find_by_location(location):
            try:
                print("Enter new location: ")
                location = input("> ")
                waterfall.location = location
                waterfall.update()
                
            except Exception as exc:
                print("Error updating waterfall", exc)
    #updating elevation property of waterfall
            print("Enter elevation to change or press enter to keep: ")
            elevation = int(input("> ") or 0)
            if waterfall:= Waterfall.find_by_elevation(elevation):
                try:
                    print("Enter new elevation number for waterfall: ")
                    elevation = int(input("> "))
                    waterfall.elevation = elevation
                    waterfall.update()
                    print(f'{waterfall.name} updated')
                except Exception as exc:
                    print(f"Error updating Elevation {waterfall.elevation} ", exc)
    #if no value: keep elevation property the same, while location and name updated
            elif elevation == 0:                 
                    waterfall = Waterfall.find_by_location(location)
                    print(f'{waterfall.name} updated')

            else:
                print("Invalid Choice")
        #updating name and keeping current location property if no value given                
        elif location == "":
            print("Enter elevation to change or press enter to keep")
        #updating value of elevation property
            elevation = int(input("> ") or 0)
            if waterfall:= Waterfall.find_by_elevation(elevation):
                try:
                    print("Enter new elevation number for waterfall")
                    elevation = int(input("> "))
                    waterfall.elevation = elevation
                    waterfall.update()
                    
                    print(f'{waterfall.name} updated')
                    
                except Exception as exc:
                    print(f"Error updating waterfall {waterfall.elevation} ", exc)
        #if no value: name property updated and location and elevation remain with current value
            elif elevation == 0:
                waterfall = Waterfall.find_by_name(name)

                print(f'{waterfall.name} updated')
        else:
            print("Invalid Choice \n")

                
    #No update for name property and updating location property
    elif name == "":
        print("Enter Town to change or press enter to keep")
        location = input("> ")
        if waterfall:= Waterfall.find_by_location(location):
            try:
                print("Enter new location: ")
                location = input("> ")
                waterfall.location = location
                waterfall.update()
            except Exception as exc:
                print("Error updating waterfall", exc)
    #updating elevation property
            print("Enter elevation to change or press enter to keep")
            elevation = int(input("> ") or 0)
            if waterfall:= Waterfall.find_by_elevation(elevation):
                try:
                    print("Enter new elevation number for waterfall: ")
                    elevation = int(input("> "))
                    waterfall.elevation = elevation
                    waterfall.update()

                    print(f'{waterfall.name} updated')
                    
                except Exception as exc:
                    print(f"Error updating waterfall {waterfall.elevation} ", exc)
        #if no value: No update for name or elevation 
            elif elevation == 0:
                waterfall = Waterfall.find_by_location(location)

                print(f'{waterfall.name} updated')
            else:
                print("Invalid Choice \n")
                
        #No update for name or location
        elif location == "":
            print("Enter elevation to change or press enter to keep")
            elevation = int(input("> ") or 0)
            if waterfall:= Waterfall.find_by_elevation(elevation):
                try:
                    print("Enter new elevation number for waterfall: ")
                    elevation = int(input(" "))
                    waterfall.elevation = elevation
                    waterfall.update()
                    
                    print(f'{waterfall.name} updated')

                except Exception as exc:
                    print(f"Error updating waterfall {waterfall.elevation} ", exc)
        #no updating for name, location, or elevation
            
            else:
                print("******Invalid Choice******\n")              

    else:
        print("******Invalid Choice******\n")

def delete_waterfall(waterfall):
        if waterfall:= Waterfall.find_by_id(waterfall.id):
            waterfall.delete()
            print(f' {waterfall.name} has been deleted!')
        else:
            print(f'Error deleting: {waterfall.name} not found')
    
def exit_program():
    print("goodbye")
    exit()


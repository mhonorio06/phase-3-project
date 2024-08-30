#!/usr/bin/env python3

from helpers import(
    exit_program,
    list_countries,
    choice_menu,
)

def main():
        
    
    menu()
    choice = input("> ")
    if choice == "c" or choice == "C":
        country_menu()            
    elif choice == "e" or choice == "E":
        exit_program()
    else:
        print("Invalid Choice")

def country_menu():
    list_countries()
    choice_menu()
    
    
def menu():
    print("***Welcome to my sightseeing app!***")
    print("Please choose from the following: \n")
    print("Press C or c to lookup countries \n")
    print("Press E or e to exit program ") 


        
if __name__ == "__main__":
    main()
    
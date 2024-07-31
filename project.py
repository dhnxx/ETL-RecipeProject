import pyfiglet
from link_scraper import scrape_and_save_recipes  
from data_extractor import check_data_availability, extract_and_save_data
from data_to_sql import run_schema_script, csv_to_sql

def main():
    user_input = None 
    while user_input != "0": 
        user_input = display_menu()  
        handle_user_choice(user_input)  

def display_menu():
    print(pyfiglet.figlet_format("ETL-Recipe", font="slant"))
    
    print("=" * 50)
    print("Select an option:")
    print("=" * 50)
    print("1. Scrape all links")
    print("2. Extract data from the links and save to CSV")
    print("3. Load raw data into SQLite database")
    print("4. Run the entire ETL Process")
    print("0. Exit Program")
    print("=" * 50)
    return get_user_choice()  

def handle_user_choice(choice):
    try:
        if choice == "1":
            print("Scraping and saving raw links...")
            scrape_and_save_links()
            print("Scraping completed successfully.")
        elif choice == "2":
            print("Extracting data from links and saving to CSV...")
            extract_and_save_links()
            print("Data extraction completed successfully.")
        elif choice == "3":
            print("Loading raw data into SQLite database...")
            load_data_to_sql()
            print("Data loading completed successfully.")
        elif choice == "4":
            print("Running the entire ETL process...")
            run_etl_process()
        elif choice == "0":
            print("Exiting Program...")
        else:
            print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_user_input(user_input):
    return user_input in ["0", "1", "2", "3", "4"]

def get_user_choice():
    """ Get user choice with validation """
    while True:
        choice = input("Enter the number corresponding to your choice: ")
        if check_user_input(choice):
            return choice
        print("Invalid choice. Please try again.")

def run_etl_process():
    """ Run the entire ETL process """
    try:
        scrape_and_save_links()
        print("Link scraping completed successfully.")
        if check_data_availability():
            extract_and_save_links()
            print("Data extraction completed successfully.")
            load_data_to_sql()
            print("Data loading completed successfully.")
            print("ETL process completed successfully.")
        else:
            print("Data not available. Please scrape links first.")
    except Exception as e:
        print(f"An error occurred during the ETL process: {e}")

def scrape_and_save_links():
    """ Scrape and save links using the scraper function """
    try:
        scrape_and_save_recipes()
    except Exception as e:
        print(f"Error during link scraping: {e}")

def extract_and_save_links():
    """ Extract data and save to CSV """
    try:
        if check_data_availability():
            extract_and_save_data()  
        else:
            print("Data not available. Please scrape links first.")
    except Exception as e:
        print(f"Error during data extraction: {e}")

def load_data_to_sql():
    """ Load raw data into SQLite database """
    try:
        run_schema_script()
        csv_to_sql()
    except Exception as e:
        print(f"Error during data loading to SQL: {e}")

if __name__ == "__main__":
    main()

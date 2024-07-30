import pyfiglet
from link-scraper import execute

def main():
    # Print the title using pyfiglet
    print(pyfiglet.figlet_format("ETL-Recipe", font="slant"))
    
    # Display options in a boxed format
    print("="*50)
    print("Select an option:")
    print("="*50)
    print("1. Scrape all links")
    print("2. Extract data from the links and save to CSV")
    print("3. Load raw data into SQLite database")
    print("="*50)
    input("Enter the number corresponding to your choice: ")


def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()
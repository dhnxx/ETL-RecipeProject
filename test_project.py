import pytest
import os
from project import check_user_input, run_etl_process, display_menu, scrape_and_save_links, extract_and_save_links, load_data_to_sql

# Test for check_user_input
def test_check_user_input():
    assert check_user_input("0") is True
    assert check_user_input("1") is True
    assert check_user_input("2") is True
    assert check_user_input("3") is True
    assert check_user_input("4") is True
    assert check_user_input("5") is False
    assert check_user_input("-1") is False

# Test for run_etl_process
def test_run_etl_process():
    # Run the ETL process
    run_etl_process()

    # Check if the expected CSV files are created
    categories = [
        "chicken",
        "pork",
        "beef",
        "vegetable",
        "dessert",
        "pasta",
        "fish",
        "noodles",
        "rice",
        "egg",
        "crab",
        "squid",
        "pulutan",
        "tofu",
        "shrimp",
    ]

    for category in categories:
        file_path = f'scraped/raw_data/{category}_recipes.csv'
        assert os.path.exists(file_path), f"{file_path} does not exist."

    # Clean up the created CSV files after the test
    for category in categories:
        file_path = f'scraped/raw_data/{category}_recipes.csv'
        if os.path.exists(file_path):
            os.remove(file_path)

# Test for scrape_and_save_links
def test_scrape_and_save_links():
    result = scrape_and_save_links()
    assert result is None  

# Test for extract_and_save_links
def test_extract_and_save_links():
    result = extract_and_save_links()
    assert result is None  

# Test for load_data_to_sql
def test_load_data_to_sql():
    result = load_data_to_sql()
    assert result is None  

if __name__ == "__main__":
    pytest.main()

import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from common.notifications.notifications import send_email
from common.src.oci.secrets import get_secret_value

def parse_ticket_number(text):
    match = re.search(r'Ticket #(\d+)', text)
    if match:
        return match.group(1)
    return None

def get_winning_ticket(url, xpath):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        element = driver.find_element(By.XPATH, xpath)
        element_text = element.text

        lines = element_text.split('\n')

        gun = lines[3]

        # Filter lines to include only those with the word "Ticket #"
        filtered_lines = [line for line in lines if "Ticket #" in line]

        number = parse_ticket_number(filtered_lines[0])

        return number, gun
    finally:
        driver.quit()

def check_and_notify_winners(ticket_number, gun, config_file='du_winner_checker/config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)

    for person, details in config.items():
        if ticket_number in details['numbers']:
            email_address = get_secret_value(details['email'])
            send_email("DU Gun Raffle Win", f"Congratulations! You are now the proud owner of a new {gun}!", email_address)
            return

    print(f"Ticket number {ticket_number} is not assigned to any user.")


du_url = "https://www.ducks.org/missouri/missouri-du-calendar-gun-giveaway"
winner_list_xpath = '//*[@id="calendarWinnerList"]'

winning_number, gun_won = get_winning_ticket(du_url, winner_list_xpath)
check_and_notify_winners(winning_number, gun_won)
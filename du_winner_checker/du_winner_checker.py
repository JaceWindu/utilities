import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

def parse_ticket_number(text):
    match = re.search(r'Ticket #(\d+)', text)
    if match:
        return match.group(1)
    return None

def get_winning_ticket_number(url, xpath):
    driver = webdriver.Chrome()
    driver.get(url)
    element = driver.find_element(By.XPATH, xpath)
    element_text = element.text

    lines = element_text.split('\n')

    # Filter lines to include only those with the word "Ticket #"
    filtered_lines = [line for line in lines if "Ticket #" in line]

    number = parse_ticket_number(filtered_lines[0])

    return number

def check_and_notify_winners(ticket_number, config_file='du_winner_checker/config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)

    for person, details in config.items():
        if ticket_number in details['numbers']:
            notify_winner(person, details['contact'])
            return

    print(f"Ticket number {ticket_number} is not assigned to any user.")

def notify_winner(winner, contact):
    print(f"Notification sent to {winner} at {contact}")

du_url = "https://www.ducks.org/missouri/missouri-du-calendar-gun-giveaway"
winner_list_xpath = '//*[@id="calendarWinnerList"]'

winning_number = get_winning_ticket_number(du_url, winner_list_xpath)
check_and_notify_winners(winning_number)
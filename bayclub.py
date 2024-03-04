import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def login(driver, username: str, password: str):
    # Log into bayclub
    username_element = driver.find_element(by=By.ID, value="username")
    username_element.send_keys(username)
    password_element = driver.find_element(by=By.ID, value="password")
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)


def select_club(driver):
    driver.implicitly_wait(5)
    plan_a_visit = driver.find_element(
        by=By.CSS_SELECTOR,
        value="div.navbar.px-0.bar-bg.py-3.clickable.ng-star-inserted",
    )
    driver.implicitly_wait(5)
    plan_a_visit.click()

    time.sleep(5)
    sf_clubs = driver.find_elements(
        by=By.CSS_SELECTOR, value="div.ml-3.size-14.black.ng-star-inserted"
    )[6]
    ssf = sf_clubs.find_element(
        By.CSS_SELECTOR, "div.d-flex.align-items-center.clickable.my-2.outline-none"
    )
    driver.implicitly_wait(5)
    ssf.click()
    continue_button = driver.find_element(
        By.CSS_SELECTOR, "div.btn.btn-light-blue.btn-block"
    )
    continue_button.click()


def select_racquet_sports(driver):
    driver.implicitly_wait(5)
    racquet_sports = driver.find_elements(By.CSS_SELECTOR, "div.m-auto")[2]
    racquet_sports.click()


def select_tennis(driver):
    driver.implicitly_wait(5)
    tennis = driver.find_element(
        By.CSS_SELECTOR,
        "div.item-tile.border-radius-8.text-center.px-1.py-3.py-lg-5.text-break.h-100.clickable",
    )
    tennis.click()
    driver.implicitly_wait(5)


def select_time_length(driver):
    driver.implicitly_wait(5)
    button_group = driver.find_elements(By.CSS_SELECTOR, "div.btn-group.w-100")[1]
    ninety_minutes = button_group.find_elements(
        By.CSS_SELECTOR, "div[class^='btn btn-outline-dark-grey size-10 py-2']"
    )[2]
    ninety_minutes.click()
    next_button = driver.find_element(
        By.CSS_SELECTOR, "button.btn.btn-info.text-uppercase.w-100.py-2.px-8"
    )
    next_button.click()
    driver.implicitly_wait(5)


def select_day(driver, day: int):
    driver.implicitly_wait(5)
    button_row = driver.find_element(
        By.CSS_SELECTOR, "div.row.w-100.h-100.no-gutters.text-center.ng-star-inserted"
    )
    day = button_row.find_elements(
        By.CSS_SELECTOR, "div.col.clickable.slider-item.align-middle.ng-star-inserted"
    )[day]
    driver.implicitly_wait(5)
    day.click()


def select_hour_view(driver):
    driver.implicitly_wait(5)
    button_group = driver.find_element(By.CSS_SELECTOR, "div.btn-group.w-100")
    hour_view = button_group.find_elements(
        By.CSS_SELECTOR, "div.btn.btn-outline-dark-grey.size-10.py-2.ng-star-inserted"
    )[1]
    driver.implicitly_wait(5)
    hour_view.click()


def select_slot(driver, start_time: str):
    driver.implicitly_wait(5)
    slot_container = driver.find_element(
        By.CSS_SELECTOR, "div.d-md-none.px-3.ng-star-inserted"
    )
    slots = slot_container.find_elements(
        By.CSS_SELECTOR,
        "div.border-radius-4.border-dark-gray.w-100.text-center.size-12.clickable.time-slot.py-2.position-relative.overflow-visible",
    )

    # reverse order to "am8:00" for ease of comparison
    start_time = start_time[-2:] + start_time[:-2]
    for slot in slots:
        slot_time_text = slot.find_element(
            By.CSS_SELECTOR,
            "div.text-lowercase",
        )
        end_time = slot_time_text.text.partition("- ")[2]
        end_time = end_time[-2:] + end_time[:-3]

        if end_time >= start_time:
            slot.click()
            driver.implicitly_wait(5)
            next_button = driver.find_element(
                By.CSS_SELECTOR, "button.btn.btn-info.text-uppercase.w-100.py-2.px-8"
            )
            next_button.click()
            return True
    return False


def confirm_booking(driver):
    driver.implicitly_wait(5)
    people_container = driver.find_element(
        By.CSS_SELECTOR, "app-racquet-sports-player-select.d-block.pb-9.pb-md-0"
    )
    person = people_container.find_element(By.CSS_SELECTOR, "div.my-1.clickable")
    person.click()
    driver.implicitly_wait(5)
    confirm_booking_button = driver.find_element(
        By.CSS_SELECTOR, "button.my-3.btn.btn-block.btn-info.text-uppercase.py-2.px-8"
    )
    confirm_booking_button.click()


def bayclub_loop(driver, day, start_time, dry_run=False):
    # loop over slot selection
    status = False
    while not status:
        select_tennis(driver)
        select_time_length(driver)
        select_day(driver, day)
        select_hour_view(driver)
        status = select_slot(driver, start_time)
        time.sleep(10)
        driver.refresh()
    if not dry_run:
        confirm_booking(driver)


def main(args):
    # Setup
    service = Service(executable_path="/Users/williamzhu/Projects/bayclub/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=100,800")
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://bayclubconnect.com/"
    driver.get(url)
    driver.implicitly_wait(10)

    login(driver, args.username, args.password)
    select_club(driver)
    select_racquet_sports(driver)

    bayclub_loop(driver, args.day, args.start_time, args.dry_run)

    time.sleep(10)
    # Clean up
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", type=str, dest="username", required=True, help="Bay Club username."
    )
    parser.add_argument(
        "-p", type=str, dest="password", required=True, help="Bay Club password."
    )
    parser.add_argument(
        "--start_time",
        type=str,
        dest="start_time",
        help="Earliest time for court to book.",
    )
    parser.add_argument(
        "-d",
        type=int,
        dest="day",
        help="Day to book.",
    )
    parser.add_argument(
        "--dry_run",
        type=bool,
        default=False,
        dest="dry_run",
        required=False,
        help="If True, don't book the court at the end.",
    )
    args = parser.parse_args()
    main(args)

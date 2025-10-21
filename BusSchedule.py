#BusSchedule.py
#Name:
#Date:
#Assignment:

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
    """
    Loads a given URL and returns the visible text from the page.
    """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    content = driver.find_element(By.XPATH, "/html/body").text
    driver.quit()
    return content

def loadTestPage():
    """
    Loads a saved test page to avoid repeated live requests.
    """
    with open("testPage.txt", 'r') as page:
        contents = page.read()
    return contents

def getHours(time):
    dt = datetime.datetime.strptime(time, "%I:%M %p")
    return dt.hour

def getMinutes(time):
    dt = datetime.datetime.strptime(time, "%I:%M %p")
    return dt.minute

def getCurrentTimeCentral():
    utc_now = datetime.datetime.utcnow()
    central_now = utc_now - datetime.timedelta(hours=5)
    return central_now

def minutesUntil(bus_time_str, current_time):
    bus_time = datetime.datetime.strptime(bus_time_str, "%I:%M %p")
    bus_time = current_time.replace(hour=bus_time.hour, minute=bus_time.minute, second=0, microsecond=0)
    if bus_time < current_time:
        bus_time += datetime.timedelta(days=1)
    delta = bus_time - current_time
    return int(delta.total_seconds() // 60)

def extractTimesFromText(text):
    lines = text.splitlines()
    times = []
    for line in lines:
        line = line.strip()
        if len(line) >= 7 and (line.endswith("AM") or line.endswith("PM")):
            try:
                datetime.datetime.strptime(line, "%I:%M %p")
                times.append(line)
            except ValueError:
                continue
    return times

def main():
    stop_number = input("Enter Stop Number: ").strip()
    route_number = input("Enter Route Number: ").strip()
    direction = input("Enter Direction (e.g., EAST, WEST, NORTH, SOUTH): ").strip().upper()

    
    url = f"https://myride.ometro.com/Schedule?stopCode={stop_number}&routeNumber={route_number}&directionName={direction}"

    
           
    content = loadTestPage()       

   
    bus_times = extractTimesFromText(content)

    
    current_time = getCurrentTimeCentral()
    print(f"\nCurrent Time: {current_time.strftime('%I:%M %p')}")

   
    upcoming = []
    for bt in bus_times:
        wait = minutesUntil(bt, current_time)
        if wait >= 0:
            upcoming.append(wait)
        if len(upcoming) == 2:
            break

    
    if upcoming:
        print(f"The next bus will arrive in {upcoming[0]} minutes.")
        if len(upcoming) > 1:
            print(f"The following bus will arrive in {upcoming[1]} minutes.")
    else:
        print("No upcoming buses found.")

if __name__ == "__main__":
    main()

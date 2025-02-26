from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

# LinkedIn giriş bilgileri (manuel giriş yapılabilir)
LINKEDIN_EMAIL = "e mail"
LINKEDIN_PASSWORD = " password"
SEARCH_QUERY = "Android Developer"

# Chrome'u başlat
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def linkedin_login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD + Keys.RETURN)
    time.sleep(5)

def search_jobs():
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={SEARCH_QUERY}"
    driver.get(search_url)
    time.sleep(3)

def scrape_jobs():
    jobs = []
    for i in range(5):  # İlk 5 sayfayı çek
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="job-search-card")

        for job in job_cards:
            title = job.find("h3", class_="base-search-card__title").text.strip()
            company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            location = job.find("span", class_="job-search-card__location").text.strip()

            jobs.append({"Title": title, "Company": company, "Location": location})

        # Sonraki sayfaya geç
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    return jobs

def save_to_csv(jobs):
    df = pd.DataFrame(jobs)
    df.to_csv("linkedin_jobs.csv", index=False)
    print("Veriler kaydedildi: linkedin_jobs.csv")

if __name__ == "__main__":
    linkedin_login()
    search_jobs()
    job_list = scrape_jobs()
    save_to_csv(job_list)
    driver.quit()

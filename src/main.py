from src.core.session import Session
from src.core.scraper import fetch_and_save_challenges, scrape_all
from src.config import BASE_URL, EMAIL, PASSWORD

def main():
    session = Session(BASE_URL, EMAIL, PASSWORD)
    challenges = fetch_and_save_challenges(session)
    scrape_all(session, challenges)


if __name__ == "__main__":
    main()
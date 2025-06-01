from session import Session
from scraper import fetch_and_save_challenges, scrape_all
from config import BASE_URL, EMAIL, PASSWORD

def main():
    """
    Entrypoint for the challenges scraper
    """
    session = Session(BASE_URL, EMAIL, PASSWORD)
    challenges = fetch_and_save_challenges(session)
    scrape_all(session, challenges)


if __name__ == "__main__":
    main()
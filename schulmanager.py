# schulmanager.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

URL = "https://login.schulmanager-online.de/#/modules/schedules/view//"
DAYS = ["Mo", "Di", "Mi", "Do", "Fr"]

class Schulmanager:
    def __init__(self, user: str, jwt: str):
        self.user = user
        self.jwt = jwt
        self.timetable = {}

    def init_timetable(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            context.add_init_script(f"""
                window.localStorage.setItem("jwt", {json.dumps(self.jwt)});
                window.localStorage.setItem("user", {json.dumps(self.user)});
            """)

            page = context.new_page()
            page.goto(URL, wait_until="networkidle")

            page.mouse.move(100, 100)
            page.mouse.move(400, 300)
            page.mouse.move(700, 400)

            page.wait_for_selector("table.calendar-table", timeout=20_000)
            page.wait_for_timeout(1000)

            html = page.evaluate("() => document.documentElement.outerHTML")
            browser.close()

        # Parse directly from the html string
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("table.calendar-table")

        for row in table.select("tbody tr"):
            period = row.select_one("th span").text.strip()
            self.timetable[period] = {}

            for day, cell in zip(DAYS, row.select("td")):
                lessons = []
                for lesson in cell.select(".lesson-cell"):
                    subject = lesson.select_one(".timetable-left span:last-child")
                    teacher = lesson.select_one(".timetable-right span span span:last-child")
                    room    = lesson.select_one(".timetable-bottom span:last-child")

                    lessons.append({
                        "subject":   subject.text.strip() if subject else lesson.select_one(".timetable-left").text.strip(),
                        "teacher":   teacher.text.strip() if teacher else "?",
                        "room":      room.text.strip() if room else "?",
                        "cancelled": "cancelled" in lesson.get("class", [])
                    })

                self.timetable[period][day] = lessons

    def get_timetable(self) -> dict:
        return self.timetable

    def get_timetable_json(self) -> str:
        return json.dumps(self.timetable, ensure_ascii=False, indent=2)
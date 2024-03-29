import copy
import os
import signal
import platform
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from models.Header import Header
from models.Commentary import Commentary
from models.Event import Event
from models.Incident import Incident
from models.InternationalCompetition import InternationalCompetition


class Scrapper:
    live_scores_page = 'http://www.livescore.com/{}/live/'
    international_competitions = "http://www.livescore.com/{}/"
    footbal_competitions = "http://www.livescore.com/"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--no-sandbox')

    name_selector = {"soccer": "",
                     "football": "",
                     "basketball": "bas-",
                     "tennis": "ten-"}
    minute_selector = {"soccer": ".min",
                       "football": ".min",
                       "basketball": "div[data-type=\"min\"]",
                       "tennis": "div[data-type=\"min\"]"}

    score_selector = {
        "basketball": "sco3",
        "tennis": "sco2"
    }

    competition_indexes = {
        "soccer": {"start": 0, "end": 1},
        "football": {"start": 0, "end": 1},
        "basketball": {"start": 0, "end": 1},
        "tennis": {"start": 0, "end": 3},
    }

    def __init__(self):
        is_windows = any(platform.win32_ver())
        if not is_windows:
            self.chrome_driver = os.path.join(os.getcwd(), "chromedrivers", "linux_chromedriver")
        else:
            self.chrome_driver = os.path.join(os.getcwd(), "chromedrivers", "win_chromedriver.exe")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chrome_driver)

    def get_live_events(self, sport):
        return self.get_competition_events("http://www.livescore.com/" + sport + "/live")

    def get_event_commentaries(self, details_link):
        self.driver.get(details_link)
        commentaries = []

        try:
            commentary_button = self.driver.find_element_by_link_text('Commentary')
        except Exception as e:
            return []
        commentary_button.click()
        minutes = self.driver.find_elements_by_class_name("comment-min")
        commentaries_list = self.driver.find_elements_by_class_name("comment")
        for commentary, mins in zip(commentaries_list[:-1], minutes[:-1]):
            i = commentary.find_element_by_tag_name("i")
            classes = i.get_attribute("class")
            event_type = classes[classes.index(" ") + 1:]
            text = commentary.text
            minute = mins.text
            commentaries.append(Commentary(text, minute, event_type))

        return commentaries

    def get_event_info(self, details_link):
        self.driver.get(details_link)

        incidents_list = []

        incidents = self.driver.find_elements_by_css_selector("div[data-type=\"incident\"]")
        for incident in incidents:
            minute = incident.find_element_by_class_name("min").text
            home = incident.find_element_by_css_selector("div[data-type=\"home\"]")
            middle = incident.find_element_by_css_selector("div[data-type=\"middle\"]")
            away = incident.find_element_by_css_selector("div[data-type=\"away\"]")

            home_player = home.find_element_by_css_selector("div[data-type=\"player-name\"]").text
            away_player = away.find_element_by_css_selector("div[data-type=\"player-name\"]").text
            score = middle.find_element_by_css_selector("span[data-type=\"score\"]").text

            away_event = middle.find_element_by_css_selector("span[data-type=\"away-icon\"]").get_attribute("class")
            home_event = middle.find_element_by_css_selector("span[data-type=\"home-icon\"]").get_attribute("class")
            incident = Incident(minute, home_player, away_player, score, home_event.split(' ')[-1],
                                away_event.split(' ')[-1])

            incidents_list.append(incident)

        # because last incident is empty
        return incidents_list[:-1]

    def get_international_competitions(self, sport):
        if sport == "soccer":
            self.driver.get(self.footbal_competitions)
        else:
            self.driver.get(self.international_competitions.format(sport))

        events = []
        tabs = self.driver.find_elements_by_css_selector("ul[data-type=\"menu\"]")

        for tab in tabs[self.competition_indexes[sport]["start"]:self.competition_indexes[sport]["end"]]:
            for child in tab.find_elements_by_tag_name("a"):
                link = child.get_attribute("href")
                name = child.text

                events.append(InternationalCompetition(name, link))

        return events

    def get_international_competition_events(self, international_competition_link):
        self.driver.get(international_competition_link)

        headers = self.driver.find_elements_by_css_selector(css_selector="div.row.row-tall")
        contents = self.driver.find_elements_by_css_selector(css_selector="div.row-gray.even")
        live_events = []
        for header, content in zip(headers, contents):
            try:
                country = header.find_element_by_tag_name(name="strong").text
                league = header.find_element_by_css_selector(css_selector="a:last-child").text

                date = header.find_element_by_class_name("right").text
                min = content.find_element_by_class_name(name="min").text

                team_names = content.find_elements_by_class_name("name")
                home_team = team_names[0].text
                away_team = team_names[1].text

                home_team_goals = content.find_element_by_class_name(name="hom").text
                away_team_goals = content.find_element_by_class_name(name="awy").text

                event_id = content.get_attribute("data-id")
                score_link = content.find_element_by_class_name("scorelink").get_attribute("href")

                event = Event(event_id, home_team, away_team, home_team_goals, away_team_goals, score_link)
                live_events.append(event)
            except Exception:
                continue

        return live_events

    def get_competition_events(self, url):
        self.driver.get(url)
        rows = self.driver.find_elements_by_css_selector("div[data-type=\"container\"]>div")
        sport = url.split("/")[3]
        events = []

        current_header = None
        for row in rows:
            data_type = row.get_attribute("data-type")
            if data_type == "stg":
                # header
                try:
                    left = row.find_element_by_class_name("left")
                    right = row.find_element_by_class_name("right")

                    links = left.find_elements_by_tag_name("a")
                    current_header = Header(links[0].text, links[0].get_attribute("href"), links[1].text,
                                            links[1].get_attribute("href"), right.text)
                except Exception as e:
                    # same competition with different date
                    right = row.find_element_by_class_name("right")
                    current_header.set_date(right.text)
            elif data_type == "evt":
                # event
                team_names = row.find_elements_by_class_name(self.name_selector[sport] + "ply")
                home_team = team_names[0].text
                away_team = team_names[1].text

                minute = row.find_element_by_css_selector(self.minute_selector[sport]).text

                if sport != "football" and sport != "soccer":
                    scores = row.find_elements_by_class_name(self.score_selector[sport])
                    home_team_goals = scores[0].text
                    away_team_goals = scores[1].text
                else:
                    home_team_goals = row.find_element_by_class_name(name="hom").text
                    away_team_goals = row.find_element_by_class_name(name="awy").text

                event_id = row.get_attribute("data-id")
                try:
                    score_link = row.find_element_by_class_name("scorelink").get_attribute("href")
                except Exception as e:
                    score_link = ""
                event = Event(event_id, home_team, away_team, home_team_goals, away_team_goals, score_link,
                              copy.deepcopy(current_header), minute)
                events.append(event)
            else:
                print("Div inside container with unknown data-type:{}".format(data_type))

        return events

    def close(self):
        self.driver.close()
        self.driver.service.process.send_signal(signal.SIGTERM)
        self.driver.quit()


if __name__ == "__main__":
    scrapper = Scrapper()
    # incidents = scrapper.get_event_info(
    #     "http://www.livescore.com/soccer/finland/veikkausliga/vps-vs-ps-kemi/1-2706760/")
    # for incident in incidents:
    #     print(incident.home_event)
    #     print(incident.away_event)
    try:
        # commentaries = scrapper.get_event_commentaries(
        #     "http://www.livescore.com/soccer/champions-league/semi-finals/real-madrid-vs-bayern-munich/1-2747587/")
        # for commentary in commentaries:
        #     print(commentary.text)
        print(scrapper.get_international_competitions("tennis"))
        print(scrapper.get_international_competitions("basketball"))
        print(scrapper.get_international_competitions("football"))
        # print(scrapper.get_competition_events("http://www.livescore.com/soccer/champions-league/"))
        # print(scrapper.get_competition_events("http://www.livescore.com/basketball/nba/"))
        # print(scrapper.get_competition_events("http://www.livescore.com/tennis/atp-1000-masters/"))
        # print(scrapper.get_live_events(sport="tennis"))
    # print(scrapper.get_competition_events("http://www.livescore.com/soccer/champions-league/"))
    # print(scrapper.get_international_competition_events("http://www.livescore.com/soccer/champions-league/"))
    # print(scrapper.get_live_events(sport="football"))
    # print(scrapper.get_live_events("http://www.livescore.com/soccer/sweden/allsvenskan/oerebro-vs-dalkurd-ff/1-2680023/"))
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        scrapper.close()

from bs4 import BeautifulSoup
import requests
import textwrap
import wikipediaapi
from cyrtranslit import to_latin

BASE_URL = "http://ftn.uns.ac.rs"
UAS = "Основне академске студије"
COURSES_LINKS_FILE = "courses_links.txt"

NEWS_PAGES = [
    "http://ftn.uns.ac.rs/996322610/fakultet-tehnickih-nauka", 
    "http://ftn.uns.ac.rs/n1761984479/fakultet-tehnickih-nauka", 
    "http://ftn.uns.ac.rs/996322612/fakultet-tehnickih-nauka"
]
NEWS_LINKS_FILE = "news_links.txt"
NEWS_FILE = "news.txt"

WIKI_TEXT_FILE = "wiki_text.txt"

FINAL_FILE = "final_text.txt"
FINAL_FILE_LAT = "final_text_lat.txt"

def scrape_courses_links():
    url = f"{BASE_URL}/688425262/studijski-programi--akreditovano-01-01-2013----01-06-2019--"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vest_div = soup.find('div', id='vest_sadrzaj_ceo')

    if vest_div:
        links = vest_div.find_all('a')
        
        with open('courses_links.txt', 'w') as f:
            for link in links:
                f.write(link.get('href') + '\n')
    else:
        print("There is not a div with an id='vest_sadrzaj_ceo'!")


def scrape_course_detailed_description(course_url):
    url = f"{BASE_URL + course_url}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vest_div = soup.find('div', id='vest_sadrzaj_ceo')
    
    if vest_div:
        return vest_div.text
    
    return ""


def scrape_course_info(course):
    response = requests.get(course)
    soup = BeautifulSoup(response.text, 'html.parser')

    affix_info_div = soup.find('div', id='affix-info')
    level_of_study = ""

    if affix_info_div:
        h4_tags = affix_info_div.find_all('h4')

        with open("courses_infos2.txt", "a", encoding='utf-8') as f:
            for h4 in h4_tags:
                if h4.find('small'):
                    small_text = h4.find('small').get_text(strip=True)
                    text_after_small = h4.text if len(h4.text) > 1 else ""
                    if "Ниво студија" in small_text:
                        level_of_study = text_after_small
                   
            a_tags = affix_info_div.find_all('a')

            if a_tags and UAS in level_of_study:
                last_a_tag = a_tags[-1]
                last_href = last_a_tag.get('href')
                f.write("\n".join(textwrap.wrap("Основне информације: " + scrape_course_detailed_description(last_href), width=120)) + "\n")
                f.write(subjects_info(course) + "\n")


def subjects_info(course):
    response = requests.get(course)
    soup = BeautifulSoup(response.text, 'html.parser')
    affix_info_div = soup.find('div', id='planTab-1').find('tbody')

    final_text = ""
    if affix_info_div:
        trs = affix_info_div.find_all('tr')

        for tr in trs:
            if "Година" in tr.text:
                h2_tag = tr.find('h2')
                if h2_tag:
                    year = h2_tag.find('span').text.strip()
                    semester = h2_tag.find_all('span')[1].text.strip()

                    final_text += ("У " + year + ". години " + semester + " семестар предмети су: \n")
            else:
                subject_name = tr.find('a').text.strip()
                details = tr.find_all('td')[1:6]

                if len(details) == 0 or details[0].get('title') is None:
                    continue

                if "Факултет техничких наука" in subject_name:
                    break

                final_text += (subject_name + " који носи " + details[-1].text + " ЕСПБ.\n")

    return final_text


def generate_courses_text():
    with open(COURSES_LINKS_FILE, 'r') as file: 
        for line in file:
            scrape_course_info(BASE_URL + line)


def scrape_news():
    for page in NEWS_PAGES:
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')
        news = soup.find_all('div', class_='col-xs-12 col-lg-4')

        with open(NEWS_LINKS_FILE, 'a', encoding='utf-8') as file:
            for n in news:
                a_tag = n.find('a')
                if a_tag:
                    href = a_tag.get('href')
                    file.write(href + "\n")


def scrape_news_text():
    news_text = ""

    with open(NEWS_LINKS_FILE, 'r') as file:
        for url in file:
            news_text += "Вест: " + scrape_course_detailed_description(url) + "\n\n"

    with open(NEWS_FILE, 'w', encoding='utf-8') as file:
        file.write(news_text)


def scrape_wiki_text():
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent='MasterRad (njegos.blagojevic@gmail.com)',
            language='sr',
            extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    p_wiki = wiki_wiki.page("Факултет техничких наука Универзитета у Новом Саду")
    with open(WIKI_TEXT_FILE, 'w', encoding='utf-8') as file:
        file.write(p_wiki.text)


def translate_to_latinic():
    with open(FINAL_FILE, 'r', encoding='utf-8') as f:
        cyrilic_text = f.read()

    translation = to_latin(cyrilic_text)
    with open(FINAL_FILE_LAT, 'w', encoding='utf-8') as f:
        f.write(translation)

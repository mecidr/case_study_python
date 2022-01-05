from urllib import parse

from PIL import Image
from io import BytesIO
import os
from bs4 import BeautifulSoup
import requests
from warnings import warn

Image.MAX_IMAGE_PIXELS = 933120000
ROOT_URL = "https://en.wikipedia.org"

city_list = ['Boston, MA', 'New York City, NY', 'Atlanta, GA', 'Charlotte, NC','Portland, OR']


def convert_city_to_wiki_article_url(city):
    # URL of the article
    page_url = ROOT_URL + "/wiki/" + city.replace(' ', '_')
    return page_url


def get_image_page(url):

    # HTML content of a page
    html_str = requests.get(url).content
    soup = BeautifulSoup(html_str, "html.parser")
    # Scans infobox element looks for first image element and copies hyperlink
    imagepath = soup.find("table", {"class": "infobox ib-settlement vcard"}).find("a", {"class": "image"}).get("href")
    if imagepath is None or "File:" not in imagepath:
        warn("No image exists or unsupported type")
    return ROOT_URL + imagepath


def get_image_source_url(url):

    # HTML content of a page
    html_str = requests.get(url).content
    soup = BeautifulSoup(html_str, "html.parser")
    # Gets original image url
    imagepath = soup.find("div", {"class": "fullMedia"}).find("a", {"class": "internal"}).get("href")
    return "https:" + imagepath


def file_name_for_city(city):
    return f"\{city.replace(' ', '_').replace(',', '')}.png"


def save_image_from_url(image_url, city):
    """Saves cropped images to current working directory"""

    # Weird header combination I've found from stackoverflow that makes it work.
    # Without this  data returned from a number of urls can not be parsed to bytes object
    # Source:
    # https://stackoverflow.com/questions/68259148/getting-404-error-for-certain-stocks-and-pages-on-yahoo-finance-python/68259438#68259438
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    }
    image_data = requests.get(image_url,headers=headers)
    byt=BytesIO(image_data.content)
    byt.seek(0)
    image = Image.open(byt)
    # adjust image size
    width, height = image.size
    if width > 500:
        width = 500
    if height > 500:
        height = 500
    # (x_offset, y_offset, width, height) defines crop area from top left
    image_crop_area = (0, 0, width, height)
    img = image.crop(image_crop_area)
    # path of the directory script has been run
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    print(current_dir_path)
    img.save(current_dir_path + file_name_for_city(city))


def get_images():

    for city in city_list:
        # article url for city
        article_url = convert_city_to_wiki_article_url(city)
        # image page url. Wiki shows images in a dedicated page for different viewing options
        image_page_url = get_image_page(article_url)
        # image source url
        image_source_url = get_image_source_url(image_page_url)
        image_source_url = image_source_url.replace('%28', '(').replace('%29', ')')
        # retrieves image, crops and saves it locally
        try:
            save_image_from_url(image_source_url, city)
            print(f"Saved image for {city}. Filename:{file_name_for_city(city)}")
        except:
            warn(f"{image_source_url} cannot be opened. City: {city}")

if __name__ == "__main__":
    get_images()

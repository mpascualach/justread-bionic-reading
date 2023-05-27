import requests
from bs4 import BeautifulSoup

def get_main_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_title = None

    header_elements = soup.select('header')
    exclude_h1_elements = []

    for header_element in header_elements:
        h1_elements = header_element.select('h1')
        exclude_h1_elements.extend(h1_elements)

    title_elements = soup.select('h1, h2, h3, h4, h5, h6')
    filtered_title_elements = [element for element in title_elements if element not in exclude_h1_elements]

    # Extract the text from the filtered title elements
    for element in filtered_title_elements:
        text = element.get_text().strip()
        if text:
            main_title = text
            break

    return main_title

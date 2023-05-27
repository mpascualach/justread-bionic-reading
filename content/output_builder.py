import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import pdb

from main_title_getter import get_main_title

def build_output(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    header_elements = soup.select('header')
    exclude_elements = []

    for header_element in header_elements:
        exclude_elements.extend(header_element.find_all(recursive=False))

    main_title = get_main_title(url) or 'Simple Read'

    paragraphs = soup.find_all('p')

    # original_article_link = None
    # canonical_link = soup.find('link', rel='canonical')['href']

    # if canonical_link is not None and 'href' in canonical_link.attrs:
    #     original_article_link = canonical_link['href']

    with open('output.html', 'w') as file:
        file.write(f'<html>\n<head>\n<title>{main_title}</title>\n')
        file.write('<link rel="stylesheet" type="text/css" href="css/styles.css">\n')
        file.write('</head>\n<body>\n')
        file.write('<div class="body">\n')

        file.write(f'<h1>{main_title}</h1>')

        # for header in headers:
        #     header_contents = header.contents
        #     header_text = ''.join(str(content) for content in header_contents if str(content).strip())
        #     title = header_text
        #     wrapped_header = f'<h1>{header_text}</h1>\n'
        #     file.write(wrapped_header)
        #     print(header)
        #     pdb.set_trace()

        # file.write(f'<p><a href="{original_article_link}" target="_blank">Read the Original Article</a></p>\n')

        for paragraph in paragraphs:
            paragraph_contents = paragraph.contents
            paragraph_text = ''.join(str(content) for content in paragraph_contents if str(content).strip())
            wrapped_paragraph = f'<p>{paragraph_text.strip()}</p>\n'
            file.write(wrapped_paragraph)

        file.write('<br>\n')

        file.write('</div>')
        file.write('</body>\n')

        file.write('</html>\n')

    output_file_path = 'output.html'
    webbrowser.open('file://' + os.path.realpath(output_file_path), new=2)
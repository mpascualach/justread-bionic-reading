import requests
from bs4 import BeautifulSoup
import re

def add_bold_to_words(sentence, percentage):
    words = sentence.split()
    bolded_sentence = []

    for word in words:
        # Skip words starting with 'href=' or '<a'
        if word.startswith('href=') or word.startswith('<a'):
            print("here")
            bolded_sentence.append(word)
            continue

        bolded_chars = int(len(word) * percentage)
        bolded_word = f"<strong>{word[:bolded_chars]}</strong>{word[bolded_chars:]}"
        bolded_sentence.append(bolded_word)

    return ' '.join(bolded_sentence)

url = 'https://www.theguardian.com/world/2023/may/18/italy-worst-flooding-in-100-years-emilia-romagna'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

headers = soup.find_all('h1')
paragraphs = soup.find_all('p')

# Extract the link to the original article
original_article_link = soup.find('link', rel='canonical')['href']

with open('output.html', 'w') as file:
    file.write('<html>\n<head>\n<title>Output</title>\n')
    file.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')
    file.write('</head>\n<body>\n')
    file.write('<div class="body">\n')

    # Write the link to the original article
    file.write(f'<p><a href="{original_article_link}" target="_blank">Read the Original Article</a></p>\n')

    for header in headers:
        header_contents = header.contents
        print(header)

    for paragraph in paragraphs:
        # Get the contents of the paragraph
        paragraph_contents = paragraph.contents

        # Wrap non-empty paragraph contents in <p> tags
        paragraph_text = ''.join(str(content) for content in paragraph_contents if str(content).strip())
            
        # if paragraph_text:
        #     bolded_paragraph = ''
        #     for word in paragraph_text.split():
        #         if word.startswith('<a'):
        #             bolded_paragraph += f'{word} '
        #         else:
        #             bolded_word = add_bold_to_words(word, 0.5)
        #             bolded_paragraph += f'{bolded_word} '

        wrapped_paragraph = f'<p>{paragraph_text.strip()}</p>\n'
        file.write(wrapped_paragraph)

    file.write('<br>\n')

    file.write('</div>')  # for <div class="body">
    file.write('</body>\n</html>')

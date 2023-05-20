import requests
from bs4 import BeautifulSoup
import re

def embolden_percentage_of_words(sentence, percentage):
    words = sentence.split()
    emboldened_sentence = []

    for word in words:

        if word.startswith('href=') or word.startswith('<a'):
            emboldened_sentence.append(word)
            continue

        emboldened_chars = int(len(word) * percentage)
        emboldened_word = f"<strong>{word[:emboldened_chars]}</strong>{word[emboldened_chars:]}"
        emboldened_sentence.append(emboldened_word)

    return ' '.join(emboldened_sentence)

url = 'https://www.theguardian.com/world/2023/may/18/italy-worst-flooding-in-100-years-emilia-romagna'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

paragraphs = soup.find_all('p')

# Choose the specific paragraph you want to experiment with
target_paragraph = paragraphs[1]

# Get the contents of the target_paragraph
paragraph_contents = target_paragraph.contents

# Extract the text and wrap it with a new <p> tag
paragraph_text = ''.join(str(content) for content in paragraph_contents)
wrapped_paragraph = f'<p>{paragraph_text}</p>'

# Create a new BeautifulSoup object from the wrapped paragraph
new_paragraph = BeautifulSoup(wrapped_paragraph, 'html.parser').find('p')

# Find all the <a> tags in the target paragraph
links = target_paragraph.find_all('a')
for link in links:
    href = link['href']
    text = link.get_text()
    a_tag = BeautifulSoup(f'<a href="{href}">{text}</a>', 'html.parser').find('a')
    
    for tag in new_paragraph.find_all('a'):
        if tag == link:
            tag.replace_with(a_tag)

# Convert the modified new_paragraph to string
 
new_paragraph_string = str(new_paragraph)

with open('output.html', 'w') as file:
    file.write('<html>\n<head>\n<title>Output</title>\n</head>\n<body>\n')
    file.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')

    file.write('<div class="body">')

    emboldened_sentence = embolden_percentage_of_words(new_paragraph_string, 0.5)

    # emboldened_sentence = re.sub(r'<a.*?>(.*?)<\/a>', r'\1', emboldened_sentence)

    file.write(f'{emboldened_sentence}\n')

    file.write('</div>')  # for <div class="body">
    file.write('</body>\n</html>')

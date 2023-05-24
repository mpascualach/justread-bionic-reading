import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from flask import Flask, render_template, request
import validators
from message_handler import start_server

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if validators.url(url):
            build_output(url)
            return render_template('success.html', url=url)
        else:
            error_message = 'Invalid URL. Please try again.'
            return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html')

def build_output(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    headers = soup.find_all('h1')
    paragraphs = soup.find_all('p')

    original_article_link = soup.find('link', rel='canonical')['href']

    with open('output.html', 'w') as file:
        file.write('<html>\n<head>\n<title>Output</title>\n')
        file.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')
        file.write('<script src="handler.js"></script>')
        file.write('</head>\n<body>\n')
        file.write('<div class="body">\n')

        for header in headers:
            header_contents = header.contents

            header_text = ''.join(str(content) for content in header_contents if str(content).strip())
            wrapped_header = f'<h1>{header_text}</h1>\n'
            file.write(wrapped_header)

        # Write the link to the original article
        file.write(f'<p><a href="{original_article_link}" target="_blank">Read the Original Article</a></p>\n')

        for paragraph in paragraphs:
            # Get the contents of the paragraph
            paragraph_contents = paragraph.contents

            # Wrap non-empty paragraph contents in <p> tags
            paragraph_text = ''.join(str(content) for content in paragraph_contents if str(content).strip())

            wrapped_paragraph = f'<p>{paragraph_text.strip()}</p>\n'
            file.write(wrapped_paragraph)

        file.write('<br>\n')

        file.write('</div>')  # for <div class="body">
        file.write('</body>\n')

        file.write('</html>\n')

    output_file_path = 'output.html'
    webbrowser.open('file://' + os.path.realpath(output_file_path), new=2)

    start_server()

if __name__ == '__main__':
    app.run()

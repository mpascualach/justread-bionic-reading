import requests
from bs4 import BeautifulSoup
import html
import webbrowser
import os

def fetch_article_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article')
    if article:
        article_asides = article.find_all('aside')
        for aside in article_asides:
            aside.decompose()

        article_figures = article.find_all('figure')
        for figure in article_figures:
            figure.decompose()

        article_blockquotes = article.find_all('blockquote')
        for blockquote in article_blockquotes:
            blockquote.decompose()

        article_footers = article.find_all('footer')
        for footer in article_footers:
            footer.decompose()

        paragraphs = article.find_all('p')
        images = article.find_all('img')

        headers = []
        header_positions = set()
        for paragraph in paragraphs:
            previous_siblings = paragraph.find_previous_siblings(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for sibling in previous_siblings[::-1]:
                if sibling not in header_positions:
                    headers.append(sibling)
                    header_positions.add(sibling)

        headers = [header for header in headers if header is not None]
    else:
        paragraphs = soup.find_all('p')
        images = soup.find_all('img')
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        headers = [header for header in headers if header is not None]

    main_title = None
    title_tag = soup.find('title')
    if title_tag:
        main_title = title_tag.get_text()

    return paragraphs, images, headers, main_title

def process_content(content):
    if isinstance(content, str):
        return html.escape(content.strip())
    elif content.name == 'a':
        tag_content = ''.join(process_content(c) for c in content.contents)
        href = content.get('href', '')
        return f'<a href="{html.escape(href)}">{tag_content}</a>'
    else:
        tag_name = content.name
        tag_style = content.get('style', '')
        tag_content = ''.join(process_content(c) for c in content.contents)
        return f'<{tag_name} style="{tag_style}"> {tag_content} </{tag_name}>'

def download_image(url, filepath):
    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, 'wb') as file:
        file.write(response.content)

def build_output(url):
    paragraphs, images, headers, main_title = fetch_article_content(url)
    output_file_path = generate_html(paragraphs, images, headers, main_title)
    open_html(output_file_path)

def generate_html(paragraphs, images, headers, main_title):
    print("Main title: ", main_title)
    output_file_path = 'output.html'

    with open('output.html', 'w') as file:
        file.write(f'<html>\n<head>\n<title>{main_title}</title>\n')
        file.write('<link rel="stylesheet" type="text/css" href="css/styles.css">\n')
        file.write('</head>\n<body>\n')
        file.write('<div class="body">\n')

        file.write(f'<h1>{html.escape(main_title)}</h1>')

        headers_written = set()

        for paragraph in paragraphs:
            sibling_headers = paragraph.find_previous_siblings(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for header in sibling_headers[::-1]:
                if header not in headers_written:
                    file.write(f'<div class="header-div">{str(header)}</div>')
                    headers_written.add(header)

            processed_content = ' '.join(process_content(c) for c in paragraph.contents)
            wrapped_paragraph = f'<p>{processed_content.strip()}</p>\n'
            file.write(wrapped_paragraph)
        
        file.write('<br>\n')

        for image in images:
            if image in paragraph.descendants:
                image_url = image['src']
                print("Image Url: ", image_url)
                image_filename = image_url.split('/')[-1]
                image_filepath = f'images/{image_filename}'
                download_image(image_url, image_filepath)

                image_tag = f'<img src="{image_filepath}" alt="Image">\n'
                file.write(image_tag)

        file.write('</div>')
        file.write('</body>\n')

        file.write('</html>\n')
    
    return output_file_path

def open_html(file_path):
    print("")
    webbrowser.open(f'file://{os.path.realpath(file_path)}', new=2)
import validators

def get_valid_url():
    while True:
        url = input("Please paste the URL for the online article: ")
        if validators.url(url):
            return url
        else:
            print("Invalid URL. Please try again.")

# Usage
article_url = get_valid_url()
print("URL:", article_url)

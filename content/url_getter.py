import validators

def get_url():
    while True:
        url = input("Paste an article link here: ")
        if validators.url(url):
            return url
        else:
            print("Nope not a valid URL.")


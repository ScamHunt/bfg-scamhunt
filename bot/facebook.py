from facebook_scraper.extractors import PhotoPostExtractor

async def handle_facebook():
    PhotoPostExtractor.extract_post_url("https://www.facebook.com/100064853824493/posts/935507685287684/?mibextid=oFDknk&rdid=pAZwSslWcE2tUTYa")
    post = extract_photo_post("https://www.facebook.com/100064853824493/posts/935507685287684/?mibextid=oFDknk&rdid=pAZwSslWcE2tUTYa",
                              options={}, request_fn=None, full_post_html=None)
    print(post)

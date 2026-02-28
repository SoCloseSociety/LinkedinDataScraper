import os

username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')
file_name = input('Enter your file name : ')

# search_query = ""
search_query = input('Enter your search query : ')
search_query = search_query.replace(" ", "%20")

place_name = input('Enter targed place name : ')
# place_name = ""
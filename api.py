import requests

API_URI = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'


def get_cover(isbn):
  api_call = requests.get(API_URI.format(isbn)).json()
  cover_uri = None

  try:
    cover_uri = api_call["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
  except KeyError:
    cover_uri = "/static/no_image.png"

  return cover_uri

import unicodedata
import pandas as pd

def strip_accents(text):
  # special case D stroke Latin: 
  text = str(text).replace("đ","d")
  text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
  return str(text)
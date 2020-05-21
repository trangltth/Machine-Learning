import unicodedata
import urllib.parse, re

def strip_accents(text):
  # special case D stroke Latin: 
  text = str(text).replace("đ","d")
  text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
  return str(text)


# URI = scheme:[//authority]path[?query][#fragment]
# scheme: = ALPHA *( ALPHAs / DIGITs / "+" / "-" / "." )
# authority   = [ userinfo "@" ] host [ ":" port ]
def parse_url(url):    
  url.lower()
  url_group = re.search('(([a-z][\w\.\-\+]*):)?(//([^/\?#:]*)(:([^/\?#]*))?/)?([^?#]*)?(\?*([^#]*))?(#?(.*))', url)
  schema = '' if url_group.group(1) is None else url_group.group(1)
  domain = '' if url_group.group(3) is None else url_group.group(3)
  port = '' if url_group.group(5) is None else url_group.group(5)
  path = '' if url_group.group(7) is None else urllib.parse.quote(url_group.group(7))
  query = '' if url_group.group(8) is None else url_group.group(8)
  second_source = '' if url_group.group(10) is None else url_group.group(10)

  return schema + domain + port + path + query + second_source
from pyfacebook import Api
import facebook
from dotenv import load_dotenv, find_dotenv
import os

# https://stackoverflow.com/questions/3084230/facebook-python-sdk-vs-pyfacebook
# https://facebook-sdk.readthedocs.io/en/latest/index.html

load_dotenv(find_dotenv())

token = os.getenv("token")
app_secret = os.getenv("app_secret")
app_id = os.getenv("app_id")

api = Api(long_term_token=token, 
          app_secret=app_secret,
          sleep_on_rate_limit= False)

print(api.get_page_info(username = 'unswmarksoc'))


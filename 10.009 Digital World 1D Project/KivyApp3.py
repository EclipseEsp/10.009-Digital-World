from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import pyrebase

url = "https://digitalworld-a7fd7.firebaseio.com/"
apikey = "AIzaSyBHXFPfYxwQSdjQh43IXWTBQLl7OxNzXcE"
urlstore ="digitalworld-a7fd7.appspot.com"
auth = "digitalworld-a7fd7.firebaseapp.com"

config = {
    "apiKey": apikey,
    "databaseURL": url,
    "authDomain": auth,
    "storageBucket": urlstore
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()
storage.child("images/canteenpic.jpeg").download(r"C:\Users\tscd1\PycharmProjects\venv\KivyApp", "canteenpic.jpeg")
canteen = database.child("canteen").get()

canteen_list = list(canteen.val()) # Get values in Firebase and turn it into a List
print("list in canteen:", canteen_list)
most_recent_key = canteen_list[len(canteen_list)-1] # Get latest entry from database
most_recent_val = database.child("canteen").child(most_recent_key).get() # Get the number of people detected from most recent photo
print(most_recent_val.val())

most_recent = "Picture Taken :   " + str(most_recent_key) # Print Date and Time of photo
print(most_recent)

canteenpic = r"C:\Users\tscd1\PycharmProjects\KivyApp\venv\canteenpic.jpeg" # Location of image stored locally
userinterface = r"C:\Users\tscd1\PycharmProjects\KivyApp\venv\userinterface.kv" # Location of kv file stored locally

canteen_count = str(most_recent_val.val())

imgurl = storage.child("images/canteenpic.jpeg").get_url(None) # it expects a token but there is none , URL for unprocessed image
imgurl2 = storage.child("opencv_images/processed_canteenpic.jpeg").get_url(None) # URL for unprocessed image

class LoadScreen(Screen): # LoadScreen Object for kv
    pass
class MainScreen(Screen): # MainScreen Object for kv
    pass
class RightScreen(Screen): # RightScreen Object for kv
    pass

class CanteenApp(App):
    temp = StringProperty('') # Variable for Parsing
    temp2 = StringProperty('') # Variable for Parsing
    temp3 = StringProperty('') # Variable for Parsing
    temp4 = StringProperty('') # Variable for Parsing
    def build(self):
        self.temp = canteen_count # Parsing canteen_count to kv language
        self.temp2 = most_recent # Parsing most_recent to kv language
        self.temp3 = imgurl # Parsing unprocessed image url to kv language
        self.temp4 = imgurl2 # Parsing processed image url to to kv language
        buildKV = Builder.load_file(userinterface) # Builder to build kv file
        return buildKV

CanteenApp().run()
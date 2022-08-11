import pyrebase
config = {
  "apiKey": "AIzaSyA1B2t25BHE2bOBbq0fVEi-EGUduENyLdM",
  "authDomain": "cmspro-67645.firebaseapp.com",
  "projectId": "cmspro-67645",
  "storageBucket": "cmspro-67645.appspot.com",
  "messagingSenderId": "886776813861",
  "appId": "1:886776813861:web:36e1972a7ec597f58be2cc",
  "measurementId": "G-TGBYD1WM2N",
    "databaseURL" :"https://console.firebase.google.com/project/cmspro-67645/settings/general/web:NWFjNDBlZTktNzFjYi00NmExLTgwNDYtYzYyZDdiNWZmODdi"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

user = auth.sign_in_with_email_and_password("CMS@avidonics.com", "123Abc2311#$")
# print('alhumdulillah')
import streamlit_authenticator as stauth
import yaml

name_list = ['meihu','cheng','admin','root','team1','team3','team4']
username_list = ['meihu','lemon','admin','root','team1','team3','team4']
passwords = ['meihu','cheng','admin','root','team1','team3','team4']

hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords)


import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])


model = genai.GenerativeModel("gemini-1.5-flash")


while True:
    myInput=input("enter here: ")
    response = model.generate_content(myInput)
    print(response.text)

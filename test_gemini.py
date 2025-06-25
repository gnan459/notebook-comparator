import google.generativeai as genai

genai.configure(api_key="AIzaSyANSRsHPcgbEtlWUv3DBEfvVrUZjbGxx4c")

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
response = model.generate_content("Hello Gemini!")
print(response.text)

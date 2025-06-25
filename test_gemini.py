import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
response = model.generate_content("Hello Gemini!")
print(response.text)

import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Function to scrape news from a website
def scrape_news(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_articles = soup.find_all('article')
        news_data = ""
        for article in news_articles:
            title = article.find('h2').text.strip()
            content = article.find('p').text.strip()
            news_data += title + " " + content + "\n\n"
        return news_data
    else:
        st.error("Failed to retrieve data.")
        return None

# Function to initialize Gemini LLM model and get responses
def get_gemini_response(prompt):
    genai.configure(api_key="AIzaSyA-71vV7XmahpYCcOq6wbD6gRfZfrEv3jc")
    model = genai.GenerativeModel("gemini-pro") 
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt, stream=True)
    return response

# Streamlit app
def main():
    st.title("News to Q&A Converter")

    # Block for scraping and displaying news articles
    st.header("1. Scrape and Display News Articles")
    url = st.text_input("Enter the URL of the website you want to scrape:")
    if st.button("Scrape News"):
        if url:
            news_text = scrape_news(url)
            if news_text:
                st.subheader("News Article:")
                st.write(news_text)
            else:
                st.warning("No news articles found.")
        else:
            st.warning("Please enter a URL.")

    # Block for generating answers based on a user-provided prompt
    st.header("2. Generate Answers from Prompt")
    prompt = st.text_area("Enter your prompt here:")
    if st.button("Get Answer"):
        if prompt:
            gemini_response = get_gemini_response(prompt)
            st.subheader("Generated Answer:")
            for chunk in gemini_response:
               
                st.write(chunk.text)
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()

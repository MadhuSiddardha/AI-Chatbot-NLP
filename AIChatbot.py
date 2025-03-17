import pandas as pd
import wikipediaapi

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

def search_dataset(question, df):
    matches = df[df['Question'].str.lower() == question.lower()]
    if not matches.empty:
        return matches.iloc[0]['Answer']
    return None

def search_wikipedia(question):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='AIChatbot/1.0', language='en')
    page = wiki_wiki.page(question)
    if page.exists() and 'artificial intelligence' in page.summary.lower():
        return page.summary[:500]  # Limit to 500 characters
    return None

def chatbot(question, df):
    answer = search_dataset(question, df)
    if answer:
        return answer
    
    wiki_answer = search_wikipedia(question)
    if wiki_answer:
        return wiki_answer
    
    return "Sorry, I can only provide information related to the topic you aksed ."

# Load dataset
df = load_dataset(r"C:\Users\kalam\Downloads\AI.csv")

# Example usage
while True:
    user_input = input("Ask a question: ")
    if user_input.lower() == 'exit':
        break
    print(chatbot(user_input, df))

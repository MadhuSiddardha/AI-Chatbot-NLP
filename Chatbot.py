import wikipedia
import json
import warnings
from bs4 import BeautifulSoup
import wikipedia.exceptions

# Suppress warnings for BeautifulSoup parsing
warnings.filterwarnings("ignore", category=UserWarning, module='beautifulsoup4')

# Function to query the local dataset
def search_in_dataset(query):
    # Expanded dataset to include AI, LLM, CV, and frameworks
    dataset = {
        "artificial intelligence": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.",
        "machine learning": "Machine learning is a branch of AI that focuses on building systems that learn from data, improve performance over time, and make predictions.",
        "deep learning": "Deep learning is a class of machine learning methods that use neural networks with many layers to analyze and interpret data.",
        "neural networks": "Neural networks are a subset of machine learning, designed to simulate the way human brains work, allowing systems to learn from data.",
        "nlp": "Natural Language Processing (NLP) is a field of AI focused on the interaction between computers and human language, enabling machines to understand and generate human language.",
        "llms": "Large Language Models (LLMs) are types of machine learning models trained for natural language tasks. They are used in various AI applications like chatbots, language translation, and text generation.",
        "computer vision": "Computer vision (CV) is a field of AI that enables machines to interpret and make decisions based on visual information from the world, such as images and videos.",
        "ai frameworks": "AI frameworks are libraries or tools that provide pre-built algorithms and models for building AI applications. Examples include TensorFlow, PyTorch, and Keras."
    }
    
    return dataset.get(query.lower(), None)  # Case insensitive match

# Function to fetch AI-related content from Wikipedia
def get_wikipedia_answer(query):
    try:
        # Special case for "nlp" to force search for Natural Language Processing
        if query.lower() == 'nlp':
            result = wikipedia.summary('Natural Language Processing', sentences=3)
            return result
        
        # Special case for "llms" to prioritize Large Language Models
        if query.lower() == 'llms':
            result = wikipedia.summary('Large language model', sentences=3)
            return result
        
        # Special case for "cv" to prioritize Computer Vision
        if query.lower() == 'cv':
            result = wikipedia.summary('Computer vision', sentences=3)
            return result

        # Special case for "ai" to prioritize Artificial Intelligence
        if query.lower() == 'ai':
            result = wikipedia.summary('Artificial Intelligence', sentences=3)
            return result
        # special case for "ml" to prioritize Machine learning
        if query.lower() =='ml':
            result =  wikipedia.summary('Machine Learning',sentences=3)
            return result
        # Special case for "dl" to prioritize Deep learning
        if query.lower() =='dl':
            result =  wikipedia.summary('Deep Learning ',sentences=3)
            return result
        

        # Attempt to fetch a summary from Wikipedia
        result = wikipedia.summary(query, sentences=3)
        
        # Check if the result contains AI-related keywords
        ai_related_keywords = ["artificial intelligence", "machine learning", "deep learning", "neural networks", "large language model", "natural language processing", "computer vision", "ai frameworks"]
        if any(keyword.lower() in result.lower() for keyword in ai_related_keywords):
            return result
        else:
            return "No AI-related information found. Please try a more specific AI query."
    
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation by checking for AI-related topics in the options
        ai_related = [item for item in e.options if 'ai' in item.lower() or 'machine learning' in item.lower() or 'deep learning' in item.lower() or 'large language model' in item.lower() or 'computer vision' in item.lower()]
        if ai_related:
            return wikipedia.summary(ai_related[0], sentences=3)
        else:
            return "Disambiguation error: No AI-related options found."
    
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Request timed out, try again later."
    except Exception as e:
        return f"Error fetching Wikipedia info: {str(e)}"

# Combined chatbot function
def chatbot(query):
    # First, try to get the answer from the dataset
    dataset_answer = search_in_dataset(query)
    if dataset_answer:
        return {"source": "dataset", "answer": dataset_answer}
    
    # If the answer isn't in the dataset, try to fetch it from Wikipedia
    wiki_answer = get_wikipedia_answer(query)
    return {"source": "Wikipedia", "answer": wiki_answer}

# Get user input for queries
while True:
    query = input("Enter your query (or type 'exit' to quit): ").strip()
    
    if query.lower() == 'exit':
        print("Exiting chatbot.")
        break
    
    result = chatbot(query)
    print(f"Query: {query}")
    print(f"Source: {result['source']}")
    print(f"Answer: {result['answer']}\n")

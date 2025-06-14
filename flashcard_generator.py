import os
import requests
import json
import re
from dotenv import load_dotenv
from utils import detect_topics

# Load environment
load_dotenv()

# Configuration
API_URL = "https://router.huggingface.co/fireworks-ai/inference/v1/chat/completions" 
HEADERS = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}"
}

def query(payload):
    """Send request to Firework API"""
    response = requests.post(
        API_URL, 
        headers=HEADERS, 
        json=payload
    )
    return response.json()

def generate_flashcards(text, subject="General"):
    """Generate flashcards using Fireworks AI's DeepSeek-R1"""
    try:
        # Detect topics for grouping
        topics = detect_topics(text)
        
        # Create prompt with delimiter-based output
        prompt = f"""Act as an expert educator creating high-impact study tools. Generate 15 detailed flashcards covering the following {subject} content. Prioritize depth, conceptual understanding, and diverse question types while adhering to this structure:

        FLASHCARD STRUCTURE:
        TOPIC: [Identify the core concept/category]
        Q: [Formulate a clear, quiz-style question]
        A: [Provide a comprehensive yet concise explanation with context]

        GUIDELINES:

        Content Coverage:
        Include definitions, key principles, real-world applications, and exceptions
        Balance factual, analytical, and inferential questions
        Vary difficulty: mix basic recall + higher-order thinking questions
        Question Types:
        "What is the definition of ___?"
        "Explain the relationship between ___ and ___"
        "Compare/contrast ___ vs ___"
        "What would happen if ___?" (scenario-based)
        "Identify the error in ___" (debugging misconception)
        Quality Standards:
        Ensure questions are unambiguous and self-contained
        Answers must include context/backing details (not single-word responses)
        Avoid repetition between cards
        Flag common misunderstandings in answers when relevant
        SOURCE MATERIAL:
        "{text[:4096]}"
        
        Flashcard:"""  # Limit to first 4096 characters to avoid token limit issues

        # Call Fireworks API
        response = query({
            "messages": [
                {"role": "system", "content": "You are a flashcard generator."},
                {"role": "user", "content": prompt}
            ],
            "model": "accounts/fireworks/models/deepseek-r1-0528",
            "max_tokens": 2048,
            "temperature": 0.3
        })

        # Extract content from response
        content = response["choices"][0]["message"]["content"]
        
        # Parse response using delimiter format
        return parse_flashcards(content, topics)
            
    except Exception as e:
        return {"error": str(e)}

def parse_flashcards(text, topics):
    """Parse flashcards using Q:/A: format"""
    cards = []
    current_card = {}
    
    lines = text.strip().split('\n')
    current_topic = topics[0] if topics else "General"
    
    for line in lines:
        line = line.strip()
        if line.startswith("TOPIC:"):
            current_topic = line.replace("TOPIC:", "").strip()
        elif line.startswith("Q:"):
            current_card["question"] = line.replace("Q:", "").strip()
        elif line.startswith("A:"):
            current_card["answer"] = line.replace("A:", "").strip()
            current_card["topic"] = current_topic
            if "question" in current_card and "answer" in current_card:
                cards.append(current_card)
            current_card = {}
    
    return cards
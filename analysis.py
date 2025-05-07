import os
from openai import OpenAI
import prompts
import dataManager

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

model = "gpt-4.1-mini-2025-04-14"
temperature = 0.2
max_tokens = 10000
topic = "paper_analysis"
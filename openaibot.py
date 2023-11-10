import os
import openai

openai.api_key = "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"

try:
    response = openai.Completion.create(
    model="babbage-002",
    prompt="What is Java Programming?",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
except Exception as e:
    print("__________________________________________________________________________")
    print(e)
    print("__________________________________________________________________________")

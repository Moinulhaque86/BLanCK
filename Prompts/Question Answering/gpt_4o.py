

import os
os.environ["OPENROUTER_API_KEY"] = "provide your GPT API(OpenRouter)"

import os
from openai import OpenAI


api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set OPENROUTER_API_KEY in environment variables.")

import pandas as pd

df = pd.read_csv("BLanCK.csv")

df

def get_answer(question, context=None):
    if context:
        question += f"শুধুমাত্র বাংলা ভাষায় এবং সর্বোচ্চ পাঁচ শব্দে উত্তর দিন, প্রশ্নটির প্রেক্ষাপট হলো {context}"
    else:
        question += "শুধুমাত্র বাংলা ভাষায় এবং সর্বোচ্চ পাঁচ শব্দে উত্তর দিন"
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    completion = client.chat.completions.create(
    model="openai/gpt-4o-2024-11-20",
    messages=[
    {
      "role": "user",
      "content": question
    }],
    temperature=0,
    max_tokens=1024,
    top_p=1
    )

    return completion.choices[0].message.content

import time
import requests
count=0
data=[["term","context","category","Culture_type","popularity","questions","answer_without_context","answer_with_context"]]
for row in df.itertuples(index=True, name='Pandas'):
    question=row.questions
    context=row.context
    try:
        ans_ques=get_answer(question,None)
        ans_ques=ans_ques.strip()
        ans_ques.replace("\n", " ")
        #--------------------------
        ans_context=get_answer(question,context)
        ans_context=ans_context.strip()
        ans_context.replace("\n", " ")
        data.append([row.term,context,row.category,row.Culture_type,row.popularity,question,correct_ans_ques,correct_ans_context])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limit exceeded. Waiting...")
            time.sleep(60)  
        else:
            print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    count+=1

    print(count)

print(data)
df_2 = pd.DataFrame(data[1:], columns=data[0])
df_2.to_csv('gpt_answers.csv', index=False)

# Verify the file has been created
print("CSV file created successfully.")
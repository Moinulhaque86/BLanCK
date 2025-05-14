

import os
os.environ["OPENROUTER_API_KEY"] ="provide your deepseek API(OpenRouter)"

import os
from openai import OpenAI

# Set API key securely
api_key = os.getenv("OPENROUTER_API_KEY")  # Ensure the key is set in the environment

if not api_key:
    raise ValueError("API key not found. Set OPENROUTER_API_KEY in environment variables.")

from openai import OpenAI

def get_answer(context=None):
    question = (
    f"{context}। এই বাক্যটিতে [MASK] শব্দটি যেখানেই আছে, "
    f"তার স্থানে বসানো যায় এমন সবচেয়ে উপযুক্ত এবং সম্ভাব্য ৫টি বাংলা শব্দ একটি Python list আকারে দাও। "
    f"শব্দগুলো এমন হবে যেন সেগুলো ওই জায়গায় বসালে বাক্যটি প্রাকৃতিক ও অর্থপূর্ণ হয়। "
    f"শুধু একটি valid Python list দাও — যেমন: ['শব্দ১', 'শব্দ২', 'শব্দ৩', 'শব্দ৪', 'শব্দ৫']। "
    f"ইংরেজি শব্দ একদমই থাকা যাবে না।"
    )


    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1
    )

    response_text = completion.choices[0].message.content

    # Evaluate the string as a list (only if you trust the response format)
    try:
        result = eval(response_text)
        if isinstance(result, list):
            return result
    except:
        pass

    return []  # fallback in case the model didn't format correctly

import pandas as pd

df = pd.read_csv("BLanCK_masked_datset.csv")

df

import time
import requests
count=0
t=0
data=[["term","masked_context","ans1","ans2","ans3","ans4","ans5","category","Culture_type"]]
for row in df.itertuples(index=True, name='Pandas'):

    context=row.masked_context
    try:
        ans=get_answer(context)
        data.append([row.term,context,ans[0],ans[1],ans[2],ans[3],ans[4],row.category,row.Culture_type])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limit exceeded. Waiting...")
            time.sleep(60)
        else:
            print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    count+=1


    if count%20==0:
        print(count)

print(data)
df_3 = pd.DataFrame(data[1:], columns=data[0])
df_3.to_csv("deepseek_masked_answers.csv", index=False)


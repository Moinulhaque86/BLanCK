

!pip install groq

import pandas as pd
from groq import Groq
import time


client = Groq(api_key="provide your LLama 3 API(Groq)")

import pandas as pd

df = pd.read_csv("BLanCK_masked_dataset.csv")

df



import ast
def get_answer(context=None):
    question = (
        f"{context}। এই বাক্যটিতে [MASK] শব্দটি যেখানেই আছে, "
        f"তার স্থানে বসানো যায় এমন সবচেয়ে উপযুক্ত এবং সম্ভাব্য ৫টি বাংলা শব্দ একটি Python list আকারে দাও। "
        f"শব্দগুলো এমন হবে যেন সেগুলো ওই জায়গায় বসালে বাক্যটি প্রাকৃতিক ও অর্থপূর্ণ হয়। "
        f"শুধু একটি valid Python list দাও — যেমন: ['শব্দ১', 'শব্দ২', 'শব্দ৩', 'শব্দ৪', 'শব্দ৫']। "
        f"ইংরেজি শব্দ একদমই থাকা যাবে না এবং কোনো ব্যাখ্যা এর দরকার নেই।"
    )

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": question}],
        temperature=0,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response_text = ""
    flag=False
    for chunk in completion:
        if (chunk.choices[0].delta.content == "['"):
            flag= True
        if flag:
            response_text += chunk.choices[0].delta.content or ""
    bangla_list = ast.literal_eval(response_text)
    return bangla_list

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

    t+=1
    if t==28:
        time.sleep(65)
        t=0

    print(count)

df_2 = pd.DataFrame(data[1:], columns=data[0])
df_2.to_csv('llama3_70b_8192_masked_answers.csv', index=False)

# Verify the file has been created
print("CSV file created successfully.")
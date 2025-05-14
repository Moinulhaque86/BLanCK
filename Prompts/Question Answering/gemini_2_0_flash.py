
pip install -U -q "google-genai"

from google import genai

from google.genai import types
import pandas as pd
import time

client = genai.Client(api_key="provide your Gemini 2.0 flash API")

import pandas as pd

df = pd.read_csv("BLanCK.csv")




def get_answer(question, context=None):
    if context:
        question += f"শুধুমাত্র বাংলা ভাষায় এবং সর্বোচ্চ পাঁচ শব্দে উত্তর দিন, প্রশ্নটির প্রেক্ষাপট হলো {context}"
    else:
        question += "শুধুমাত্র বাংলা ভাষায় এবং সর্বোচ্চ পাঁচ শব্দে উত্তর দিন"

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=question,
        config=types.GenerateContentConfig(
            max_output_tokens=1024,
            top_k=1,
            top_p=1.0,
            temperature=0.0,
            response_mime_type='application/json',
            seed=42,
        ),
    )

    return response.text

import time
import requests
count=0
t=0

data=[["term","context","category","Culture_type","popularity","questions","answer_without_context","answer_with_context"]]
for row in df.itertuples(index=True, name='Pandas'):
    question=row.questions
    context=row.context
    try:
        ans_ques=get_answer(question,None)
        ans_ques=ans_ques.strip()
        ans_ques.replace('"',"")
        correct_ans_ques=''
        checking=ans_ques.split()
        if "{" in checking:
            for i in range(2,len(checking)-1):
                correct_ans_ques+=checking[i]+" "
        else:
            for i in range(1,len(checking)-1):
                correct_ans_ques+=checking[i]+" "
        correct_ans_ques.strip()
        correct_ans_ques=correct_ans_ques[1:len(correct_ans_ques)-2]
        #--------------------------
        ans_context=get_answer(question,context)
        ans_context=ans_context.strip()
        ans_context.replace('"',"")
        correct_ans_context=''
        checking=ans_context.split()
        if "{" in checking:
            for i in range(2,len(checking)-1):
                correct_ans_context+=checking[i]+" "
        else:
            for i in range(1,len(checking)-1):
                correct_ans_context+=checking[i]+" "
        correct_ans_context.strip()
        correct_ans_context=correct_ans_context[1:len(correct_ans_context)-2]

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

    t+=1
    if t==7:
        time.sleep(65)
        t=0

df_2 = pd.DataFrame(data[1:], columns=data[0])
df_2.to_csv('Gemini_answers.csv', index=False)

# Verify the file has been created
print("CSV file created successfully.")
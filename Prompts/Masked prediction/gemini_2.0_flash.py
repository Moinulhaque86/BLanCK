
pip install -U -q "google-genai"

from google import genai

from google.genai import types
import pandas as pd
import time

client = genai.Client(api_key="provide your Gemini 2.0 flash API")

import pandas as pd

df = pd.read_csv("BLanCK_masked_dataset.csv")

df

def get_answer(context=None):
    question="নিম্নলিখিত বাক্যের জন্য একটি শব্দের উত্তর দিয়ে [MASK] পূরণ করুন:"+context+"return only word and give 5 possible answers in word and give the five answers in a single python list not nested python list. Do not give more than five and do not forget to close brackets"
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
    print(response.text)
    return response.text

import time
import ast


data = [["term", "masked_context", "score_1", "score_2", "score_3", "score_4", "score_5","category","Culture_type", "result"]]
count = 0
t = 0

for row in df.itertuples(index=True, name='Pandas'):
    term = row.term
    masked_context = row.masked_context


    ans = get_answer(masked_context)

    if term in ans:
        result = "True"
    else:
        result = "False"


    print("Raw answer:", ans)

    try:

        list_start = ans.find('[')
        list_end = ans.find(']', list_start) + 1


        list_str = ans[list_start:list_end]


        print("Extracted list string:", list_str)


        inner_list = ast.literal_eval(list_str)

        if len(inner_list) == 5:
            score_1, score_2, score_3, score_4, score_5 = inner_list
        elif len(inner_list) == 1:

            score_1 = inner_list[0]
            score_2 = score_3 = score_4 = score_5 = "None"


    except (ValueError, SyntaxError) as e:

        score_1 = score_2 = score_3 = score_4 = score_5 = None
        print(f"Error processing answer: {e}")

    data.append([term, masked_context, score_1, score_2, score_3, score_4, score_5,row.category,row.Culture_type,result])

    print("Count:", count)
    count += 1
    t += 1

    if t == 14:
        time.sleep(65)
        t = 0

import csv

csv_file = 'gemini_2.0_flash_masked_prediction.csv'


# Write data to CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file '{csv_file}' created successfully.")
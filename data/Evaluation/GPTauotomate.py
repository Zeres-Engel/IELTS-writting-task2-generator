import openai
import random
import json
import time
from tqdm import tqdm
import matplotlib.pyplot as plt

def get_api_key(key_list):
    return random.choice(key_list)

def automate(sample, key_list):
    api_key = get_api_key(key_list)
    openai.api_key = api_key
    prompt = f"Please evaluate the IELTS Writing Task 2 essay and provide the corresponding score.\n\nEssay: {sample}\n\n---\n\nScore:"
    try:
        while True:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=64,
                n=1,
                stop="\n",
                temperature=0.2,
            )
            answer = response.choices[0].text.strip()
            score_start_index = answer.find(":") + 1
            score_string = answer[score_start_index:].strip()
            try:
                score = float(score_string)
                return score
            except ValueError:
                pass
    except Exception as e:
        print(f"Error: {e}. Retrying in 10 seconds...")
        time.sleep(10)

try:
    # get API keys
    with open("APIkeys.txt", 'r',  encoding='UTF-8') as keys_file:
        key_list = [key.strip() for key in keys_file.readlines()]
    # read data
    with open("train.json", "r", encoding="UTF-8") as data_file:
        data_series = [sample.strip() for sample in data_file.readlines() if sample.strip()]
        data_series = [sample.replace("[", "").replace("]", "") for sample in data_series]

    cnt = 0
    not_good = []
    total_score = 0
    with tqdm(total=len(data_series), desc="Scoring") as pbar:
        for sample in data_series[cnt:]:
            if sample:
                IELTS_score = automate(sample, key_list)
                cnt += 1
                if IELTS_score >= 6.5:
                    total_score += 1
                else:
                    not_good.append(sample)
                    with open("not_good_sample.json", "w") as outfile:
                        json.dump(not_good, outfile)
                pbar.update(1)
                # Tính toán số lượng bài viết đạt điểm và không đạt điểm
                num_passed = total_score
                num_failed = cnt - total_score
                # Xuất biểu đồ Pie Chart ra hình ảnh

except Exception as e:
    print(f"An error occurred: {e}")
    plot_pie_chart(num_passed, num_failed)


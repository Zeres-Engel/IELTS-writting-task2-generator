import openai
import random
import pandas as pd
import time

def get_api_key(key_list):
    return random.choice(key_list)

def check_answer(answer, sample):
    words = answer.count(' ')
    s_words = sample.count(' ')
    if words < 249 or words > s_words:
        return False
    return True

def ask_question(sample, key_list):
    api_key = get_api_key(key_list)
    openai.api_key = api_key
    words = sample.count(' ')
    prompt = f"rewrite an essay follows IELTS writing task 2 format band score 7. or higher, about {words + 500} words and depending on this essay: {sample}"
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            answer = response.choices[0].text.strip()
            answer = str(answer)
            answer = answer.replace('\n', ' ')
            return answer
        except Exception as e:
            print(f"Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)
            continue

if __name__ == "__main__":
    number_generator = 5702
    while True:
        try:
            keys = open("APIkeys.txt", 'r',  encoding='UTF-8')
            key_list = []
            for key in keys.readlines():
                key_list.append(key.strip())
            keys.close()
            data_series = pd.read_json('train.json', typ='series')
            
            start = len(data_series) - number_generator
            
            for i in range (start, number_generator):
                
                new_essay = ask_question(data_series[i], key_list)
                while check_answer(new_essay, data_series[i]) is False:
                    new_essay = ask_question(data_series[i], key_list)
                data_series.loc[number_generator + i] = new_essay
                data_series.to_json('train.json')
                print(i)
        except Exception as e:
            data_series.to_json('train.json')
            print(f"An error occurred: {e}")
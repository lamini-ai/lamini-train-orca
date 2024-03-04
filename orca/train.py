import lamini
from lamini import Lamini

from datasets import load_dataset

from tqdm import tqdm

def train():
    model_name = "roneneldan/TinyStories-1M"

    con = {
        "production.url": "https://api.staging.powerml.co",
        "production.key": "c4f0834ec7bbedde1822e1ae0ba2abaa9999728d",
    }

    llm = Lamini(model_name=model_name, config=con)

    data = load_data()

    llm.upload_data(data)

    llm.train(use_cached_model=False, is_public=True)

def load_data():

    data = []
    hf_dataset = "Open-Orca/OpenOrca"

    num_rows = 1000
    dataset = load_dataset(hf_dataset, split="train", streaming=True)

    n_excess = 0
    input_data = ""
    for idx, row in tqdm(enumerate(dataset), total=num_rows):
        if idx >= num_rows:
            break
        sys_prompt = row["system_prompt"]
        question = row["question"]
        answer = row["response"]
        prompt = construct_prompt(sys_prompt, question)
        point = {"input": prompt, "output": answer}
        input_data += prompt + "\n" + answer + "\n"
        if len(str(point)) > 30000:
            print(f"index {idx} len: ", len(str(point)))
            print("EXCESS")
            n_excess += 1
            continue
        data.append(point)
    print("\ndata len: ", len(data))
    print("\nn excess: ", n_excess)

    return data


def construct_prompt(sys_prompt, question):
    return f"""### System:
{sys_prompt}
### Human:
{question}
### Assistant:
"""


train()

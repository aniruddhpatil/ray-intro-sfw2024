import sys

import ray
import time

from datasets import load_dataset
from pprint import pprint
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

ray.init(address="ray://0.0.0.0:10001")

# https://huggingface.co/datasets/conll2003
dataset = load_dataset("conll2003", split="validation")
shuffled_dataset = dataset.shuffle(seed=23022024)
sentences = [' '.join(tokens) for tokens in shuffled_dataset[:1]["tokens"]]


# https://huggingface.co/dslim/bert-base-NER?library=transformers
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer, batch_size=1, device=-1)

example_sentence = "I enjoy living in Karnataka!"

pprint(nlp(example_sentence))


def serial_predict(sentence):
    return nlp(sentence)


@ray.remote(scheduling_strategy="SPREAD")
def distributed_predict(pipe, sentence):
    return pipe(sentence)


serial_start = time.time()
serial_predictions = []
for sentence in sentences:
    serial_predictions.append(serial_predict(sentence))
print("Normal Time {}".format(time.time() - serial_start))

ray_start = time.time()
pipe_ref = ray.put(nlp)
ray_predictions_ref = [distributed_predict.remote(pipe_ref, sentence) for sentence in sentences]
print("Ray Time {}".format(time.time()-ray_start))
ray_square_list = ray.get(ray_predictions_ref)

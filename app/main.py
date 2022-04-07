from typing import ForwardRef
from fastapi import FastAPI, Form
from pydantic import BaseModel
import re
import uvicorn

app = FastAPI()
def jaccard_similarity(A, B): #calculating the jaccarrd similarity
    nominator = A.symmetric_difference(B)
    denominator = A.union(B)
    similarity = 1 - len(nominator)/len(denominator)
    return round(similarity,3)

def cleaner(array, index_val): #excluding special characters.	
	for iterator in range(len(array[index_val])):
		array[index_val][iterator] = re.sub("[',.?]","",array[index_val][iterator]) 
	return set(array[index_val]) #converting to set

def create_utterance_and_intent(raw_data_):
	utterance_ = [] # list of sets for each utterance in raw_data
	intent_ = [] # list of sets for each intent in raw_data
	index = 0
	
	for given_type in raw_data_['chatLog']:
		
		utterance_.append(given_type['utterance'].split(" "))
		utterance_[index] = cleaner(utterance_,index)
		index += 1

		intent_.append(given_type['intent'])
	
	return utterance_, intent_

raw_data = {
  "chatLog": [
    {
      "utterance": "Hi, Mario's what can I get you?",
      "intent": "Greeting"
    },
    {
      "utterance": "I'd like to order a pizza for pickup please.",
      "intent": "HowCanIHelp"
    },
    {
      "utterance": "OK, what would you like to order?",
      "intent": "ReadyToReceiveOrder"
    },
    {
      "utterance": "I'd like a medium supreme pizza.",
      "intent": "OrderItem"
    },
    {
      "utterance": "Anything more?",
      "intent": "AnyMoreItems"
    },
    {
      "utterance": "Also, a garlic bread.",
      "intent": "OrderItem"
    },
    {
      "utterance": "Is that all?",
      "intent": "AnyMoreItems"
    },
    {
      "utterance": "Yes, that is all thanks.",
      "intent": "EndOfOrder"
    },
    {
      "utterance": "OK, your order is a medium supreme and a garlic bread.",
      "intent": "ConfirmItem"
    },
    {
      "utterance": "Should be ready in about 30 minutes.",
      "intent": "DurationBeforePickupAnswer"
    },
    {
      "utterance": "Thank you, goodbye.",
      "intent": "Goodbye"
    }
  ]
} # given raw_data of chatlogs

utterance_set, intent_set = create_utterance_and_intent(raw_data)

@app.get("/health")
def read_root():
    return 200

@app.post("/detect_intent/")
def detect_intent(message: str=Form(...)):
    user_input = [message.split(" ")]
    user_set = cleaner(user_input,0)
    max_similarity = -1
    max_iterator = 0
    for iterator in range(len(utterance_set)):
        value = jaccard_similarity(user_set,utterance_set[iterator])
        if max_similarity <= value:
            max_similarity = value
            max_iterator = iterator
    return {"Intent: ", intent_set[max_iterator]}


if __name__ == "__main__":
    uvicorn.run(app, port = 8000, host = "0.0.0.0")

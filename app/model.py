import requests

API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
headers = {"Authorization": f"Bearer {'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'}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	


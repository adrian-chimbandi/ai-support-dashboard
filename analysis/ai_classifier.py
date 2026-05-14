import os, json, time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a support ticket classifier for a money transfer service. Respond ONLY with valid JSON in this exact format, nothing else: {"category": "...", "sentiment": "..."} Categories: Payment Issue, Verification, Refund, Technical Problem, Account Access, Other Sentiments: frustrated, neutral, positive"""

def classify_with_ai(message):
try:
response = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": SYSTEM_PROMPT},
{"role": "user", "content": message}
],
max_tokens=60,
temperature=0
)
return json.loads(response.choices[0].message.content)
except:
return {"category": "Other", "sentiment": "neutral"}

def classify_all(df, cache='data/classified_tickets.csv'):
import pandas as pd
if os.path.exists(cache):
return pd.read_csv(cache) # Use cached results, don't call API again
results = []
for _, row in df.iterrows():
r = classify_with_ai(row['message'])
r['ticket_id'] = row['ticket_id']
results.append(r)
time.sleep(0.5) # Pause between API calls
out = pd.DataFrame(results)
df.merge(out, on='ticket_id').to_csv(cache, index=False)
return pd.read_csv(cache)
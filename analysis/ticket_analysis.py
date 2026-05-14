import pandas as pd

FRUSTRATED_WORDS = [
    'unacceptable', 'furious', 'disgusted', 'terrible',
    'scam', 'fraud', 'useless', 'angry', 'disappeared',
    'still waiting', 'been days', 'been weeks', 'not working'
]
POSITIVE_WORDS = ['thank you', 'great', 'excellent', 'perfect', 'resolved']
URGENT_PHRASES = ['urgently', 'urgent', 'immediately', 'wrong number', 'disappeared']


def load_tickets(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df['message'] = df['message'].str.strip()
    return df


def detect_sentiment(message):
    msg = message.lower()
    if any(w in msg for w in FRUSTRATED_WORDS):
        return 'frustrated'
    elif any(w in msg for w in POSITIVE_WORDS):
        return 'positive'
    else:
        return 'neutral'


def detect_urgency(message):
    msg = message.lower()
    return any(p in msg for p in URGENT_PHRASES)


def categorize_ticket(message):
    msg = message.lower()
    if any(w in msg for w in ['transfer', 'payment', 'pending', 'send', 'sent']):
        return 'Payment Issue'
    elif any(w in msg for w in ['verify', 'verification', 'id']):
        return 'Verification'
    elif any(w in msg for w in ['refund', 'money back']):
        return 'Refund'
    elif any(w in msg for w in ['crash', 'error', 'app', 'broke']):
        return 'Technical Problem'
    elif any(w in msg for w in ['account', 'access', 'password', 'locked', 'suspended', 'pin']):
        return 'Account Access'
    else:
        return 'Other'


def enrich_tickets(df):
    df['category'] = df['message'].apply(categorize_ticket)
    df['sentiment'] = df['message'].apply(detect_sentiment)
    df['is_urgent'] = df['message'].apply(detect_urgency)
    return df


def find_automation_candidates(df):
    total = len(df)
    counts = df['category'].value_counts()
    candidates = []
    for category, count in counts.items():
        pct = round(count / total * 100, 1)
        score = 3 if pct >= 20 else 1
        if category in ['Verification', 'Account Access']:
            score += 2
        candidates.append({
            'category': category,
            'count': count,
            'percentage': pct,
            'automation_score': score
        })
    return pd.DataFrame(candidates).sort_values('automation_score', ascending=False)

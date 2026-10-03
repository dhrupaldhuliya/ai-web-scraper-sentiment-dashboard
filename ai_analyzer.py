

import re
from textblob import TextBlob


def analyze_sentiment(text: str) -> dict:
    """
    Return polarity (-1 negative to +1 positive), subjectivity (0 factual
    to 1 opinionated), and a human-readable label.
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    if polarity > 0.15:
        label = "Positive"
    elif polarity < -0.15:
        label = "Negative"
    else:
        label = "Neutral"

    return {"polarity": polarity, "subjectivity": subjectivity, "sentiment": label}


_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "of", "to", "in", "on",
    "and", "or", "but", "it", "this", "that", "with", "for", "as", "be",
    "have", "has", "had", "i", "you", "we", "they", "he", "she", "not",
}


def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """
    Pull out lightweight keywords: unique, non-stopword words longer than
    3 characters, in order of appearance. Uses a plain regex tokenizer
    (rather than TextBlob's) so it works with zero extra data downloads.
    """
    words = [w.lower() for w in re.findall(r"[A-Za-z]+", text) if len(w) > 3]
    keywords = [w for w in dict.fromkeys(words) if w not in _STOPWORDS]
    return keywords[:top_n]


def enrich_records(records: list[dict]) -> list[dict]:
    """Attach sentiment + keywords to every scraped record."""
    enriched = []
    for record in records:
        sentiment = analyze_sentiment(record["text"])
        keywords = extract_keywords(record["text"])
        enriched.append({**record, **sentiment, "keywords": ", ".join(keywords)})
    return enriched


if __name__ == "__main__":
    sample = [{"text": "The world as we have created it is a process of our thinking."}]
    print(enrich_records(sample))

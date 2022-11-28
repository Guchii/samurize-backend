from typing import List

import spacy
import wikipedia
from nltk.tokenize import BlanklineTokenizer
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from youtube_transcript_api import YouTubeTranscriptApi

nlp = spacy.load("en_core_web_sm")

path = "./data"  # 'google/pegasus-cnn_dailymail'
tokenizer = PegasusTokenizer.from_pretrained(path)
text_model = PegasusForConditionalGeneration.from_pretrained(path)


def get_paragraphs(text):
    return BlanklineTokenizer().tokenize(text)


def get_tokens(paragraph):
    return tokenizer(
        paragraph, truncation=True, padding="longest", return_tensors="pt"
    )


def summarize(tokens):
    summary = text_model.generate(**tokens)
    summary = tokenizer.decode(summary[0])
    return summary


def generate_video_tokens(transcript):
    doc = nlp(transcript)
    sentences = [sent.text for sent in doc.sents]

    video_tokens = []
    for i in range(0, len(sentences), 5):
        video_tokens.append(get_tokens(sentences[i : i + 5]))  # NOQA
    return video_tokens


def get_transcript(transcript):
    subtitles = ""
    for words in transcript:
        subtitles += words["text"]
        subtitles += " "
    return subtitles


def video_summary(url: str):
    iv = url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(iv)
    transcript = get_transcript(transcript)
    video_tokens = generate_video_tokens(transcript)
    return [summarize(token) for token in video_tokens]


def wiki_summary(title: str):
    wk = wikipedia.page(title)
    content = wk.content.splitlines()[:3]
    return generate_summary(content)


def generate_summary(content: List[str]):
    tokens = [get_tokens(c) for c in content]
    summaries = [summarize(t) for t in tokens]
    return summaries

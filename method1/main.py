from newspaper import Article
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

url = 'https://www.sciencedaily.com/releases/2022/09/220929133431.htm'
article = Article(url)
article.download()
article.parse()

def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS) and word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

text = "\n".join(article.text.split("\n\n"))

with open("method1/article.txt", "w") as text_file:
    print(text, file=text_file)
with open("method1/summary.txt", "w") as text_file:
    print(summarize(text, 0.2), file=text_file)
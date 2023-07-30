import os
import json
from somajo import SoMaJo
from bs4 import BeautifulSoup
from gensim.models import Word2Vec
#from gensim.models import Phrases #for bigrams

def transform_corpus(foldername):
    """
    Transforms the json data into tokenized text that can be used to train the word embeddings.

    :param string foldername: Name of the folder in which the json files are stored
    :return: A list of all sentences as list of their tokens
    :rtype: list of list of str
    """

    tokenized_sentences = []

    tokenizer = SoMaJo("de_CMC", split_camel_case=True)

    if not os.path.exists(foldername):
        raise Exception("Folder does not exist")

    for filename in os.listdir(foldername):
        if filename.endswith(".json"):
            file = open(foldername + "/" + filename, 'r', encoding="utf-8")
            data = json.load(file)

            if not "results" in data:
                file.close()
                continue

            for decision in data["results"]:
                if not "content" in decision:
                    file.close()
                    continue

                content = decision["content"]
                soup = BeautifulSoup(content, features="lxml")
                txt = soup.text.lower()
                sentences = tokenizer.tokenize_text([txt])

                for sentence in sentences:
                    tokenized_sentence = []

                    for token in sentence:
                        tokenized_sentence.append(token.text)

                    tokenized_sentences.append(tokenized_sentence)

            file.close()
        else:
            continue
    return tokenized_sentences

def train_model(foldername, vector_size=300, window=5, min_count=1, workers=4):
    """
    Use gensim to train a Word2Vec model with the corpus in the provided folder and store it.

    :param string foldername: Name of the folder in which the json files are stored
    :param int vector_size: Size of the embeddings
    :param int window: Window size used to train the embeddings
    :param int min_count: Minimum occurences for a word the be included
    :param int workers: Number of workers used by gensim
    """

    sentences = transform_corpus(foldername)

    model = Word2Vec(vector_size=vector_size, window=window, min_count=min_count, workers=workers) # parameter name vector_size or size depending on gensim version

    # for bigrams
    # bigram_transformer = Phrases(tokenized_sentences)
    # model.build_vocab(bigram_transformer[tokenized_sentences])

    #unigrams
    model.build_vocab(sentences)
    total_examples = model.corpus_count
    model.train(sentences=sentences, total_examples=model.corpus_count, epochs=model.epochs, report_delay=1.0,
                total_words=model.corpus_total_words)
    model.wv.save_word2vec_format(foldername + "/" + foldername + '.mod', binary=True)

train_model("1991-1991")
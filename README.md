# Diachronic Word Embeddings from German Court Decisions

This project provides code to train diachronic Word2Vec embeddings from German court decisions, provided by [Open Legal Data](https://openlegaldata.io/), with gensim and visualise context shifts with [pgfplots](https://ctan.org/pkg/pgfplots). The code is part of the paper [Tracking Semantic Shifts in German Court Decisions with Diachronic Word Embeddings](https://aclanthology.org/2022.nllp-1.19/). The alginment of different vector spaces uses code from [Zhicong Chen](https://gist.github.com/zhicongchen/9e23d5c3f1e5b1293b16133485cd17d8).

## Usage

For usage examples check the file [usage.py](usage.py).

### downloader
Downloads court decisions from the Open Legal Data API for the given timespan (always starting with the 1st of January and ending with the 31st of December)
```
# download data from 1991
downloader.download(1991,1991)

# download data from the 80s
downloader.download(1980,1989)
```

### trainer
Trains a Word2Vec model with gensim on a previously downloaded data set
```
# train model with the data from 1991
trainer.train_model("1991-1991")

# train model with the data from the 80s
trainer.train_model("1980-1989")
```

### comparison

Find most similar words for the word "haus" in different timespans
```
comparison.synonyms("haus", ["1980-1989", "1990-1999"])
```

Calculate cosine similarity between "haus" and "wohnen" in the 80s and the 90s
```
comparison.cosine_similarity_over_time("haus", "wohnen", ["1980-1989", "1990-1999"])
```

Visualise the context shift of the word "haus" from the 80s to the 90s (make sure that LaTeX binaries are part of the path variable)
```
comparison.context_shift("haus", ["1980-1989", "1990-1999"])
```

## Citation information
```
@inproceedings{braun-2022-tracking,
    title = "Tracking Semantic Shifts in {G}erman Court Decisions with Diachronic Word Embeddings", 
    author = "Braun, Daniel",
    booktitle = "Proceedings of the Natural Legal Language Processing Workshop 2022",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates (Hybrid)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.nllp-1.19",
    pages = "218--227",
    abstract = "Language and its usage change over time. While legal language is arguably more stable than everyday language, it is still subject to change. Sometimes it changes gradually and slowly, sometimes almost instantaneously, for example through legislative changes. This paper presents an application of diachronic word embeddings to track changes in the usage of language by German courts triggered by changing legislation, based on a corpus of more than 200,000 documents. The results show the swift and lasting effect that changes in legislation can have on the usage of language by courts and suggest that using time-restricted word embedding models could be beneficial for downstream NLP tasks.",
}

```
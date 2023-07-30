# usage examples

import comparison
import downloader
import trainer

# download data from the 80s
downloader.download(1980, 1989)
# train model with the data from the 80s
trainer.train_model("1980-1989")

# download data from the 90s
downloader.download(1990, 1999)
# train model with the data from the 90s
trainer.train_model("1990-1999")

# find most similar words for the word "haus" in both models
print(comparison.synonyms("haus", ["1980-1989", "1990-1999"]))

# calculate cosine similarity between "haus" and "wohnen" in the 80s and the 90s
print(comparison.cosine_similarity_over_time("haus", "wohnen", ["1980-1989", "1990-1999"]))

# visualise the context shift of the word "haus" from the 80s to the 90s
comparison.context_shift("haus", ["1980-1989", "1990-1999"])
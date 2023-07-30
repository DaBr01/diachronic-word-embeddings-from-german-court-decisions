from gensim.models import KeyedVectors
from numpy import dot
from numpy.linalg import norm
from sklearn.decomposition import PCA
from align import smart_procrustes_align_gensim
import matplotlib
from matplotlib import pyplot

matplotlib.use("pgf") # make sure that latex binaries are part of the path variable
matplotlib.rcParams.update({
    "pgf.texsystem": "xelatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})



def synonyms(word, foldernames, n=5):
    """
    Returns the n most similar words for the given word for each of the provided models.

    :param str word: Word for which synonyms are searched
    :param list of str foldernames: List of the foldernames in which the models are located
    :return: A list of the n most similar words for the given word for each of the provided models
    :rtype: list of list of tuples
    """

    synonym_list = []

    for foldername in foldernames:
        model = KeyedVectors.load_word2vec_format(foldername + "/" + foldername + ".mod", binary=True)
        synonym_list.append(model.most_similar(positive=[word], topn=n))

    return synonym_list

def cosine_similarity_over_time(word1, word2, foldernames):
    """
    Returns the cosine similarity between the two words for each of the models

    :param str word1: First word for which to calculate the cosine similarity
    :param str word2: Second word for which to calculate the cosine similarity
    :param list of str foldernames: List of the foldernames in which the models are located
    :return: A list of the cosine similarity between the two words for each of the given models
    :rtype: list of floats
    """

    similarity = []

    for foldername in foldernames:
        model = KeyedVectors.load_word2vec_format(foldername + "/" + foldername + ".mod", binary=True)
        a = model.word_vec(word1)
        b = model.word_vec(word2)

        cos_sim = dot(a, b) / (norm(a) * norm(b))
        similarity.append(cos_sim)

    return similarity

def context_shift(baseword, foldernames, n=4):
    """
    For each word that should be analysed, we calculate the union of the word’s k nearest neighbours in each decade.
    We then mathematically align and map the different models into a shared two-dimensional system of coordinates, using Principle Component Analysis (PCA).
    We then plot the vector for the word that we want to analyse in each decade in this system of coordinates.
    As suggested by Hamilton et al. (2016) we only plot the most “modern” vector for the nearest neighbours, simplifying the plot.
    See paper for more details.

    :param str word: Word for which synonyms are searched
    :param list of str foldernames: List of the foldernames in which the models are located
    :param int n: Number of neighbours from each period to include in the context
    """

    models = [] # list of all models
    sim_words = [] # list of most similar words from all models

    for foldername in foldernames:
        models.append(KeyedVectors.load_word2vec_format(foldername + "/" + foldername + ".mod", binary=True))

    for model in models[:-1]:
        model = smart_procrustes_align_gensim(models[-1], model) # align models into one vector space

    # gather list of most similar words from all models
    for m in models:
        sim = []
        if baseword in m.vocab:
            sim = m.most_similar(positive=[baseword], negative=[], topn=n, restrict_vocab=None)

        for s in sim:
            if not s[0] in sim_words and s[0] in models[-1].vocab: # check if word is not yet in the list and in the vocabulary of the most recent model
                sim_words.append(s[0])

    X = []
    all_words = []

    # add vectors of all context words based on the latest model
    for word in sim_words:
        m = models[-1] # most recent model
        X.append(m[word])
        all_words.append(word)

    # add vectors for the investigated word from each individual model
    for index, m in enumerate(models):
        if baseword in m.vocab:
            X.append(m[baseword])
            all_words.append(baseword + "-" + foldernames[index]) # mark the source model of the vector

    pca = PCA(n_components=2) # PCA to enable visualisation
    result = pca.fit_transform(X)

    # create visualisation using pyplot
    pyplot.figure(figsize=(6, 6))

    for i, word in enumerate(all_words):
        x = result[i, 0]
        y = result[i, 1]

        if i >= len(sim_words):
            pyplot.plot(x,y, 'rs')
        else:
            pyplot.plot(x, y, 'bo')
        pyplot.annotate(word, xy=(x, y), textcoords="offset points", xytext=(0,10))

    for i, word in enumerate(all_words):
        x = result[i, 0]
        y = result[i, 1]
        if i > len(sim_words):
            pyplot.arrow(result[i-1, 0],result[i-1, 1],x - result[i-1, 0], y - result[i-1, 1], color="grey", length_includes_head=True, head_width = 0.01, width = 0.001)

    pyplot.savefig(baseword + '.pgf')
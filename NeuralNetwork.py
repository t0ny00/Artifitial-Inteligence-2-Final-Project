from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.pipeline import make_pipeline
import itertools
import warnings
from os import walk
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, './MSongsDB/PythonSrc')
import hdf5_getters as getters




def extractSongData(file_name, getters_to_apply):
    path = './canciones/' + file_name + '.h5'
    h5 = getters.open_h5_file_read(path)
    song = np.empty(0)
    for get in getters_to_apply:
        res = getters.__getattribute__(get)(h5)
        song = np.append(song, np.mean(res))
    h5.close()
    return song

def transformIntoBinary(data):
    binary_data = list(data)
    for i in range(len(data)):
        if(data[i] != "Rock"): binary_data[i] = True
        else: binary_data[i] = False
    return binary_data

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')



if __name__ == '__main__':

    warnings.filterwarnings("ignore")
    songs = []
    genres = []
    genres_labels = ["Electronic","Pop","Rap","Rock"]
    all_songfiles_dict = {}

    list_of_getters = filter(lambda x: x[:4] == 'get_', getters.__dict__.keys())
    getters_to_remove = ['get_song_id', 'get_release', 'get_artist_hotttnesss', 'get_title', 'get_artist_longitude',
                         'get_artist_id', 'get_artist_7digitalid',
                         'get_artist_terms_freq', 'get_similar_artists', 'get_artist_terms_weight',
                         'get_artist_familiarity','get_song_hotttnesss',
                         'get_artist_name', 'get_artist_playmeid', 'get_artist_mbtags', 'get_year',
                         'get_artist_location', 'get_audio_md5', 'get_artist_mbid', 'get_track_7digitalid',
                         'get_artist_terms', 'get_artist_mbtags_count', 'get_release_7digitalid',
                         'get_track_id', 'get_num_songs', 'get_artist_latitude']

    getters_to_apply = list(set(list_of_getters).symmetric_difference(set(getters_to_remove)))


    # Aqui va el codigo para iterar

    all_songs_file = open('lista_final.cls','r')

    for line in all_songs_file:
        act_line = line.split('\t')
        all_songfiles_dict[act_line[0]] = act_line[1][:-1]

    all_songs_file.close()

    f = []
    for (dirpath, dirnames, filenames) in walk('canciones'):
        f.extend(filenames)
        break

    print "Accessing song's data... \n"
    for elem in f:
        file_name = elem[:-3]                              # nombre del archivo de la cancion sin la extension
        genre = all_songfiles_dict[file_name]              # Genero de la cancion
        song = extractSongData(file_name,getters_to_apply) # retorna los datos de la cancion
        if not (np.isnan(np.sum(song))):
            songs.append(song)
            genres.append(genre)



    # ============ Preparing data and model=======================

    genres_binary = transformIntoBinary(genres)
    neural_network = MLPClassifier(solver='adam', alpha=1e-2, hidden_layer_sizes=(100,100,100), max_iter=5000, verbose=False)
    clf = make_pipeline(preprocessing.StandardScaler(), neural_network)

    # =========== All vs All model (Rock vs Pop vs Rap vs Electronic) ============================

    print 'Training All vs All model (Rock vs Pop vs Rap vs Electronic) \n'
    predicted = cross_val_predict(clf, songs, genres, cv=10)

    print "============ PERFORMANCE RESULTS ============= \n"
    acc = metrics.accuracy_score(genres, predicted)
    confusion = metrics.confusion_matrix(genres, predicted)
    f1 = metrics.f1_score(genres,predicted,average="micro")
    print 'Accuracy = %.4f || F1 = %.4f\n' % (acc,f1)
    plt.figure()
    plot_confusion_matrix(confusion,classes=genres_labels,title="Confusion Matrix for all genres label model")
    plt.show()



    # =========== Binary Classification (Rock vs Not Rock) ==================

    print '\nTraining Binary Classification (Rock vs Not Rock) \n'
    predicted = cross_val_predict(clf, songs, genres_binary, cv=10)

    print "============ PERFORMANCE RESULTS ============= \n"
    acc = metrics.accuracy_score(genres_binary, predicted)
    recall = metrics.recall_score(genres_binary, predicted,average='micro')
    roc = metrics.roc_auc_score(genres_binary, predicted)
    confusion = metrics.confusion_matrix(genres_binary, predicted)
    f1 = metrics.f1_score(genres_binary, predicted)
    print 'Accuracy = %.3f || Roc = %.3f || F1 = %.4f\n' % (acc,roc,f1)
    plt.figure()
    plot_confusion_matrix(confusion, classes=["Rock","Not Rock"], title="Confusion Matrix for Rock vs Not Rock label")
    plt.show()




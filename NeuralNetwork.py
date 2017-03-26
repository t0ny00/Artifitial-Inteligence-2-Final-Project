from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from os import walk
import sys
import numpy as np
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


if __name__ == '__main__':

    songs = []
    genres = []
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
    temp = []
    for elem in f:
        file_name = elem[:-3]                              # nombre del archivo de la cancion sin la extension
        genre = all_songfiles_dict[file_name]              # Genero de la cancion
        song = extractSongData(file_name,getters_to_apply) # retorna los datos de la cancion
        songs.append(song)
        genres.append(genre)
        temp.append(file_name)


    # for i in range(len(songs)):
    #     print("\nCancion: " + str(i+1) + ' ' + str(songs[i]) + "\nGenero: " + str(genres[i]) + '\n')

    scaler = StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(songs, genres, test_size = 0.33)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(1000, 1000,1000,100))
    clf.fit(X_train , y_train)

    print accuracy_score( clf.predict(X_test),y_test)
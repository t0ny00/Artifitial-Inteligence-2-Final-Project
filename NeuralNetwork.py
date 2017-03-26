from sklearn.neural_network import MLPClassifier
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

    list_of_getters = filter(lambda x: x[:4] == 'get_', getters.__dict__.keys())
    getters_to_remove = ['get_song_id', 'get_release', 'get_artist_hotttnesss', 'get_title', 'get_artist_longitude',
                         'get_artist_id', 'get_artist_7digitalid',
                         'get_artist_terms_freq', 'get_similar_artists', 'get_artist_terms_weight',
                         'get_artist_familiarity',
                         'get_artist_name', 'get_artist_playmeid', 'get_artist_mbtags', 'get_year',
                         'get_artist_location', 'get_audio_md5', 'get_artist_mbid', 'get_track_7digitalid',
                         'get_artist_terms', 'get_artist_mbtags_count', 'get_release_7digitalid',
                         'get_track_id', 'get_num_songs', 'get_artist_latitude']

    getters_to_apply = list(set(list_of_getters).symmetric_difference(set(getters_to_remove)))


    # Aqui va el codigo para iterar

    file_name = #nombre del archivo de la cancion sin la extencion
    song = extractSongData(file_name,getters_to_apply) # retorna los datos de la cancion
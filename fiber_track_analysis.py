import shelve


def import_data():
    shelf_file = shelve.open('fiber-track-data-py')
    fiber_track_data = shelf_file['data']
    shelf_file.close()
    return fiber_track_data


data = import_data()
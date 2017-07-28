import dill as pickle


def save_object(filename, obj):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def retrieve_object(filename):
    with open(filename, 'rb') as input_data:
        obj = pickle.load(input_data)
    return obj

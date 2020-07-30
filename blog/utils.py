import uuid

def get_filename(filename):
    extension = filename.split('.')[1]
    if len(filename.split('.')) != 2:
        raise TypeError("image seems currupted...")
    if not extension in ['jpg', 'jpeg']:
        raise TypeError("we currently accept jpg/jpeg formats only.")
    unique_name = uuid.uuid4().hex

    return unique_name+'.'+extension
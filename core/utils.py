def user_img(instance, filename):
    """
    Function to define the upload path for user avatars.

    Args:
        instance: Instance of the User model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the avatar.
    """

    return f'user_{instance.id}/{filename}'

def user_dir(instance, filename):
    """
    Function to define the upload path for files associated with the user.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file.
    """

    return f'user_{instance.owner.id}/{filename}'

def user_dir_playlist_song(instance, filename):
    """
    Function to define the upload path for files associated with a playlist's song.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file.
    """

    return f'user_{instance.playlist.owner.id}/{filename}'

def user_dir_album_song(instance, filename):
    """
    Function to define the upload path for files associated with an album's song.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file.
    """

    return f'user_{instance.album.owner.id}/{filename}'

def get_upload_path(instance, filename):
    """
    Function to get the upload path based on the instance and filename.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file based on the instance type.
    """

    if hasattr(instance, 'playlist'):
        return user_dir_playlist_song(instance, filename)
    else:
        return user_dir_album_song(instance, filename)

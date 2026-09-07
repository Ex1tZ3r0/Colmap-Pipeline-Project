class MissingBinaries(Exception):
    """ Raised if required binary files are missing. """
    pass

class NoMedia(Exception):
    """ Raised if no compatible video files are found. """
    pass
    
class FileProcessingError(Exception):
    """ Raised if file processing fails """
    pass
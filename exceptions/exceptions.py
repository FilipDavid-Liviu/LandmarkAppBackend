class LandmarkNotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class InvalidFileTypeError(Exception):
    pass

class FileProcessingError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class SavedLandmarkError(Exception):
    pass

class DatabaseError(Exception):
    pass

class LandmarkAlreadySavedError(Exception):
    pass

class LandmarkNotSavedError(Exception):
    pass
from django.core.exceptions import ValidationError

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webm']
FILE_SIZE_LIMIT = 20


def size_validator(file):
    file_size = file.size / (1024 ** 2)
    
    if file_size > FILE_SIZE_LIMIT:
        raise ValidationError(f'File size should not exceed {FILE_SIZE_LIMIT} MB.')
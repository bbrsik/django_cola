import uuid
import os
from django.core.files.uploadedfile import SimpleUploadedFile


def change_filename(file):
    old_filename = str(file.name)
    temp_filename = old_filename.split('.')
    new_filename = str(uuid.uuid4()) + '.' + temp_filename[-1]
    renamed_file = SimpleUploadedFile(new_filename, file.read(), content_type=file.content_type)
    return renamed_file


def delete_file(file_name):
    path = "./media/" + str(file_name)
    os.remove(path)
    return 0


def validate_user_password(request, user):
    if not user.is_authenticated:
        # something that refuses to continue the profile edit procedure
        return False
    if not user.check_password(request.POST.get('password')):
        request.session['edit_failed'] = True
        return False
    return True

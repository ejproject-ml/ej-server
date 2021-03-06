import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.utils.six import BytesIO

from ej_users.models import User


def create_image(filename, size=(100, 100), image_mode='RGB',
                 image_format='png'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.name = filename
    data.seek(0)
    return data


@pytest.fixture
def logged_client(db):
    user = User.objects.create_user('email@server.com', 'password')
    client = Client()
    client.force_login(user)
    return client


class TestEditProfile:
    def test_user_logged_access_edit_profile(self, logged_client):
        resp = logged_client.get('/profile/edit/')
        assert resp.status_code == 200

    def test_user_logged_edit_profile_picture(self, logged_client):
        avatar = create_image('avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        form_data = {'name': 'Maurice', 'profile_photo': avatar_file, 'gender': 0, 'race': 0}

        response = logged_client.post('/profile/edit/', form_data)
        assert response.status_code == 302 and response.url == '/profile/'
        user = User.objects.get(email='email@server.com')
        assert user.profile.profile_photo.name

from django.test import TestCase
from django.urls import reverse

from .models import user_img, user_dir, User, PlayList, Song


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='testuser', 
            email='test@email.com', 
            password='testpassword', 
            name='test user'
        )
        
    def test_user_content(self):
        user = User.objects.get(id=1)
        expected_name = f'{user.name}'
        expected_email = user.email
        expected_avatar = f'user_{user.id}/avatar.svg'
        
        self.assertEqual(expected_name, 'test user')
        self.assertEqual(expected_email, 'test@email.com')
        self.assertEqual(expected_avatar, f'user_{user.id}/avatar.svg')

    def test_user_img_function(self):
        user = User.objects.get(id=1)
        result = user_img(user, 'test.jpg')
        expected_result = f'user_{user.id}/test.jpg'

        self.assertEqual(result, expected_result)

    def test_user_str_method(self):
        user = User.objects.get(id=1)
        result = user.__str__()
        expected_result = 'test user'

        self.assertEqual(result, expected_result)

# class PlayListModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         user = User.objects.create_user(
#             username='testuser', 
#             email='test@example.com', 
#             password='testpassword', 
#             name='Test User'
#         )
#         PlayList.objects.create(playlist_name='Test Playlist', owner=user, genre='Test Genre')

#     def test_playlist_str_method(self):
#         playlist = PlayList.objects.get(id=1)
#         result = playlist.__str__()
#         expected_result = 'Test Playlist'

#         self.assertEqual(result, expected_result)

#     def test_playlist_user_dir_function(self):
#         playlist = PlayList.objects.get(id=1)
#         user = playlist.owner
#         result = user_dir(playlist, 'test.jpg')
#         expected_result = f'user_{user.id}/test.jpg'

#         self.assertEqual(result, expected_result)

# class SongModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         user = User.objects.create_user(
#             username='testuser', 
#             email='test@example.com', 
#             password='testpassword', 
#             name='Test User'
#         )

#         playlist = PlayList.objects.create(playlist_name='Test Playlist', owner=user, genre='Test Genre')

#         Song.objects.create(song_name='Test Song', playlist=playlist, music_file='test.mp3')

#     def test_song_str_method(self):
#         song = Song.objects.get(id=1)
#         result = song.__str__()
#         expected_result = 'Test Song'

#         self.assertEqual(result, expected_result)

    # def test_song_user_dir_song_function(self):
    #     song = Song.objects.get(id=1)
    #     playlist = song.playlist
    #     user = playlist.owner
    #     result = user_dir_song(song, 'test.mp3')
    #     expected_result = f'user_{user.id}/test.mp3'

    #     self.assertEqual(result, expected_result)

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='secret')
    
    def test_login(self):
        response = self.client.post(reverse('core:login'), {'username':'testuser', 'password':'secret'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_signup(self):
        response = self.client.post(reverse('core:signup'), {
            'name': 'Test User2',
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password1': 'p4s4W)rd12B',
            'password2': 'p4s4W)rd12B'
        })
        print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:home'))

    def test_logout(self):
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

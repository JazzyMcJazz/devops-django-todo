from django.test import TestCase, Client
from django.contrib.auth.models import User
from todo.models import Todo

class TodoTestCase(TestCase):

    def setUp(self):
        alice = User.objects.create_user(username='alice', password='wyx123wyx')
        bob = User.objects.create_user(username='bob', password='xyz123xyz')

        self.alice = alice
        self.bob = bob

        Todo.objects.create(user=alice, text='Kill the cat')
        Todo.objects.create(user=alice, text='Fry a potato')
        Todo.objects.create(user=alice, text='Make a todo app')
        Todo.objects.create(user=bob, text='Kill the cat')
        Todo.objects.create(user=alice, text='Learn to speak Chinese')
        Todo.objects.create(user=alice, text='Plan dinnerparty')
        Todo.objects.create(user=alice, text='Make an omlet')
        Todo.objects.create(user=bob, text='Buy plane ticket')
        Todo.objects.create(user=bob, text='Apply for tourist visa')
        Todo.objects.create(user=bob, text='Bake a cake')
        Todo.objects.create(user=alice, text='Kill the cat')

    def test_number_of_todos(self):
        assert Todo.objects.count() == 11

    def test_number_of_users(self):
        assert User.objects.count() == 2

    def test_user_number_todos(self):
        assert Todo.objects.filter(user=self.alice).count() == 7
        assert Todo.objects.filter(user=self.bob).count() == 4


    def test_user_can_login_see_items_create_and_delete(self):
        c = Client()
        # login
        response = c.get('/', follow=True)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'registration/login.html')
        response = c.post('/accounts/login/',
                          {'username':'alice', 'password':'wyx123wyx'},
                          follow=True)
        assert response.status_code == 200
        # inspect todos/
        self.assertTemplateUsed(response, 'todo/index.html')
        assert b'Learn to speak Chinese' in response.content
        assert response['content-type'] == 'text/html; charset=utf-8'
        # post new item
        response = c.post('/todos/',
                          {'text':'Post a todo via test client'},
                          follow=True)
        assert response.status_code == 200
        assert b'Post a todo via test client' in response.content
        # delete item
        response = c.delete('/todos/12/', follow=True)
        # inspect todos/ for deleted item
        assert b'Post a todo via test client' not in response.content
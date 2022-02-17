from urllib import response
from django.test import TestCase, Client

from books.models import Book,Category
class BookTest(TestCase):
    def setUp(self):
        Book.objects.create()
        Book.objects.create()

    def tearDown(self):
        Book.objects.all().delete()
        
    def test_total_book_list_get_success(self):
        books = Book()
        category = {
            'id' : '1', 
            'name' : '한국'
        }
        response = books.get('/books', json.dumps(category),content_type='application/json')
        self.assertEqaul(response.json(),
            {
                'message' : 'success'
            }
        )

    def test_nation_book_list_get_success(self):
        books = Book()
        category = {
            'id' : '1', 
            'name' : '한국'
        }
        response = books.get('/books', json.dumps(category),content_type='application/json')
        self.assertEqaul(response.json(),
            {
                'result' : 'success'
            }
        )
        self.assertEqual(response.status_code,200)

    def test_filter_book_list_get_success(self):
        self.assertEqual(response.status_code, 200)
        
    def test_authorkview_get_invalid_key(self):
        client = Client()
        author = {
            'first_name'  : 'Guido van Rossum',
            'email'       : 'GuidovanRossum@gmail.com'
        }
        response = client.post('/book/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )
        self.assertEqual(response.status_code,400)
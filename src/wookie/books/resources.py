from flask_restful import Resource


class Books(Resource):
    """
    Resource for all the books
    """
    def get(self):
        """
        Return a JSON array of all books
        """
        books = [{'title': 'Paok'}]
        return {'count': len(books), 'items': books}, 200

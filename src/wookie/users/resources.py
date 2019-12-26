from flask_restful import Resource, fields, marshal_with, request, abort
from flask_jwt_extended import create_access_token


class BaseResource(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs['logger']
        self.users_dao = kwargs['users_dao']


auth_dto = {'access_token': fields.String}


class UserAuthentication(BaseResource):
    """
    Resource for authenticating a User
    """
    @marshal_with(auth_dto, envelope='data')
    def post(self):
        """
        Return a JWT token after the user is authenticated
        """
        self.logger.info('POST /auth')
        auth_data = request.get_json()
        if 'username' not in auth_data or 'password' not in auth_data:
            abort(400)
        user = self.users_dao.find_user_by_credentials(auth_data['username'],
                                                       auth_data['password'])
        if not user:
            abort(403)
        access_token = create_access_token(identity=user['id'])
        return {'access_token': access_token}, 200

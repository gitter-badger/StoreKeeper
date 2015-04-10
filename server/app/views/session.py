from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user

from app.models import User
from app.modules.example_data import ExampleUsers
from app.modules.view_helper import get_validated_request, RequestProcessingError
from app.serializers import UserSerializer, SessionDeserializer
from app.server import config, api
from app.views.common import api_func


class SessionView(restful.Resource):
    @api_func('Get current session', url_tail='sessions',
              response=ExampleUsers.ADMIN.get())
    def get(self):
        user = User.query.filter_by(username=g.user.username).first()
        return UserSerializer(user).data

    @api_func('Login user', url_tail='sessions',
              login_required=False,
              request=ExampleUsers.ADMIN.set(['username', 'password']),
              response=ExampleUsers.ADMIN.get(),
              status_codes={401: 'bad authentication data or user is disabled',
                            422: 'there is wrong type / missing field'})
    def post(self):
        try:
            data = get_validated_request(SessionDeserializer())
        except RequestProcessingError as e:
            abort(422, message=e.message)

        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            abort(401, message='login error')
        if not login_user(user):
            abort(401, message='login error')
        return UserSerializer(user).data, 201

    @api_func('Logout user', url_tail='sessions',
              response=None)
    def delete(self):
        logout_user()
        return


api.add_resource(SessionView, '/%s/api/sessions' % config.App.NAME, endpoint='sessions')

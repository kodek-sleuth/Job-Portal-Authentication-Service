from __future__ import print_function
import os
import json
from flask import make_response, jsonify, request, redirect
from linkedin_v2.linkedin import LinkedInAuthentication, LinkedInApplication, PERMISSIONS


authentication = LinkedInAuthentication(os.getenv('LINKEDIN_API_KEY'), os.getenv('LINKEDIN_API_SECRET'),
                                        os.getenv('LINKEDIN_RETURN_URL'), ["r_liteprofile"])

def get_linkedin_auth_url():
    """
        Collects user profile and verifies email.
    """
    return authentication.authorization_url

def get_linkedin_auth_data():
    code = request.args.get('code')
    authentication.authorization_code = code
    token = authentication.get_access_token()
    application = LinkedInApplication(token=token)
    data = application.get_profile()
    return {'data': data}

    # try:
    #     user_in_db = User.objects(auth_type='linkedin').first()  # check for existence of user
    #     if not user_in_db:
    #         User(email="None", name=f"{data['localizedFirstName']} {data['localizedLastName']}",
    #              is_verified=True, auth_type="linkedin",
    #              password=bcrypt.generate_password_hash(user_data['id'], 10)).save()
    #         return {'message': 'successfully signed up user'}
    #     else:
    #         return {'message': 'successfully signed in user'}
    # except Exception as error:
    #     return make_response(jsonify({'error': error}), 500)

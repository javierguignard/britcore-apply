# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request, jsonify, abort, make_response

# local import

from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()

def create_app(config_name):
    from app.models import FeatureRequest

    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    def dummy_loguin(auth_key):
        #TODO PUT LOGUIN METHOD
        return True

    DUMMY_AREAS = {
            'policies': 'Policies',
            'billing': 'Billing',
            'claims': 'Claims',
            'reports': 'Reports',
        }
    @app.route('/api/areas/', methods=['GET'])
    def dummy_areas():
        r = make_response(jsonify(DUMMY_AREAS))
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r

    DUMMY_CLIENT_MAP = {
                '1': 'Client A',
                '2': 'Client B',
                '8': 'Client C',
            }

    @app.route('/api/clients/', methods=['GET'])
    def dummy_clients():
        if request.method == "GET":
            r = make_response(jsonify(DUMMY_CLIENT_MAP))
            r.headers.add('Access-Control-Allow-Origin', '*')
            return r

    @app.route('/api/features_requests/', methods=['POST', 'GET'])
    def feature_requests():
        if request.method == "POST":
            if not dummy_loguin(''):
                response = {
                    'message': 'You need loguin!'
                }
                return make_response(jsonify(response)), 301
            title = request.data.get('title', False)
            description = str(request.data.get('description', ""))
            product_area = request.data.get('product_area', False)
            client_id = request.data.get('client_id', False)
            client_priority = int(request.data.get('client_priority', 1))
            try:
                date_target = datetime.strptime(request.data.get('date_target', ''), '%Y-%m-%d')
            except ValueError as error:
                date_target = None

            if title and product_area and client_id and date_target:
                fr = FeatureRequest.query.filter_by(client_id=client_id, client_priority=client_priority).first()

                if fr is not None:
                    response = jsonify({
                        'message': 'Exists priority {} for client "{}" '.format(client_priority, DUMMY_CLIENT_MAP[client_id])
                        })
                    return make_response(response),402
                fr = FeatureRequest(title=str(title))
                fr.description = description
                fr.product_area = str(product_area)
                fr.client_id = int(client_id)
                fr.client_priority = int(client_priority)
                fr.date_target = date_target
                fr.save()
                priority_to_update = client_priority
                features_to_update_count = FeatureRequest.query.filter_by(client_id=client_id,
                                                                          client_priority=priority_to_update).count()
                while features_to_update_count > 1:
                    feature_to_update = FeatureRequest.query.filter_by(client_id=client_id,
                                                                       client_priority=priority_to_update).order_by(
                        'id').first()
                    feature_to_update.client_priority = feature_to_update.priority + 1
                    priority_to_update = priority_to_update + 1
                    feature_to_update.save()
                    features_to_update_count = FeatureRequest.query.filter_by(client_id=client_id,
                                                                              client_priority=priority_to_update).count()

                response = jsonify({
                    'id': fr.id,
                    'title': fr.title,
                    'description': fr.description,
                    'product_area': fr.product_area,
                    'client_id': fr.client_id,
                    'client_priority': fr.client_priority,
                    'date_target': fr.date_target,
                })
                r = make_response(response)
                r.headers.add('Access-Control-Allow-Origin', '*')
                return r, 201
            else:
                response = jsonify({'message': 'Error, need some parameters',
                            'title': title,
                            'description': description,
                            'product_area': product_area,
                            'client_id': client_id,
                            'client_priority': client_priority,
                            'date_target': date_target,
                            })
                r = make_response(response)
                r.headers.add('Access-Control-Allow-Origin', '*')
                return r, 401

        if request.method == "GET":
            # GET
            # get all the feature_requests
            results = []
            all_fr = FeatureRequest.query.all()
            for fr in all_fr:
                obj = {
                    'id': fr.id,
                    'title': fr.title,
                    'description': fr.description,
                    'product_area': fr.product_area,
                    'client_id': fr.client_id,
                    'client_priority': fr.client_priority,
                    'date_target': fr.date_target.strftime('%Y-%m-%d'),
                }
                results.append(obj)
            r = make_response(jsonify(results))
            r.headers.add('Access-Control-Allow-Origin', '*')
            return r, 200


        else:
            response = {
                'message': 'Error, please contact administrator'
            }
            r = make_response(jsonify(response))
            r.headers.add('Access-Control-Allow-Origin', '*')
            return r, 401

    @app.route('/api/feature_requests/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
    def feature_requests_manipulation(id, **kwargs):
        print(request)
        fr = FeatureRequest.query.filter_by(id=id).first()
        if not dummy_loguin(''):
            response = {
                'message': 'You need loguin!'
            }
            return make_response(jsonify(response)), 301
        if not fr:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == "GET":

            r = make_response(jsonify({
                       "message": "{}".format(fr)
                   }))
            r.headers.add('Access-Control-Allow-Origin', '*')
            return r, 200

        elif request.method == "DELETE":
            fr.delete()
            r = make_response(jsonify({
                "message": 'Feature Request deleted'
            }))
            r.headers.add('Access-Control-Allow-Origin', '*')
            return r, 200

        elif request.method == 'PUT':

            title = request.data.get('title', False)
            description = request.data.get('description', False)
            client_priority = request.data.get('client_priority', False)
            try:
                date_target = datetime.strptime(request.data.get('date_target', ''), '%Y-%m-%d')
            except ValueError as error:
                date_target = False

            if title:
                fr.title = title
            if description:
                fr.description = description
            if client_priority:
                fr.client_priority = client_priority
            if date_target:
                fr.date_target = date_target

            fr.save()
            response = {
                'id': fr.id,
                'title': fr.title,
                'description': fr.description,
                'product_area': fr.product_area,
                'client_id': fr.client_id,
                'client_priority': fr.client_priority,
                'date_target': fr.date_target,
            }
            r = make_response(jsonify(response))
            r.headers.add('Access-Control-Allow-Origin', '*')
            return r, 200

        else:
            response = {
                'message': 'Error, please contact administrator'
            }
            return make_response(jsonify(response)), 401

    return app

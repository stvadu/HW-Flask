from __future__ import annotations
import requests
from hashlib import md5
from typing import Union
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advertisment
from schema import CreateAdvertisment, PatchAdvertisment, Validation
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask("app")

class HttpError(Exception):
    def __init__(self, status_code: int, message: Union[dict, list, str]):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {"status": "error", "description": error.message}
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_d = model_obj.dict(exclude_none=True)
    except ValidationError as errr:
        raise HttpError(400, message=errr.errors())
    return model_obj_d


def get_advertisment(session: Session, advertisment_id: int):
    advertisment = session.get(Advertisment, advertisment_id)
    if advertisment is None:
        raise HttpError(404, message="Advertisment doesn't exist!")
    return advertisment


def hash_password(password: str):
    password = password.encode()
    password_hash = md5(password)
    password_hash_str = password_hash.hexdigest()
    return password_hash_str


class AdvertismentView(MethodView):
    def get(self, advertisment_id: int):
        with Session() as session:
            advertisment = get_advertisment(session, advertisment_id)
            return jsonify(
                {
                    "id": advertisment.id,
                    "title": advertisment.title,
                    "text": advertisment.text,
                    "author": advertisment.author,
                    "creation_date": advertisment.creation_date.isoformat(),
                }
            )

    def delete(self, advertisment_id: int):
        with Session() as session:
            advertisment = get_advertisment(session, advertisment_id)
            session.delete(advertisment)
            session.commit()
            return jsonify({"status": "success"})

    def post(self):
        json_data = validate_json(request.json, CreateAdvertisment)
        with Session() as session:
            advertisment = Advertisment(**json_data)
            session.add(advertisment)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "This advertisment is already exists!")
            return jsonify({"id": advertisment.id})

    def patch(self, advertisment_id: int):
        json_data = validate_json(request.json, PatchAdvertisment)
        with Session() as session:
            advertisment = get_advertisment(session, advertisment_id)
            for field, value in json_data.items():
                setattr(advertisment, field, value)
            session.add(advertisment)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "This advertisment is already exists!")
            return jsonify(
                {
                    "id": advertisment.id,
                    "title": advertisment.title,
                    "text": advertisment.text,
                    "author": advertisment.author,
                    "creation_date": advertisment.creation_date.isoformat(),
                }
            )


app.add_url_rule(
    "/ad/<int:advertisment_id>",
    view_func=AdvertismentView.as_view("with_advertisment_id"),
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule(
    "/ad/",
    view_func=AdvertismentView.as_view("create_advertisment"),
    methods=["POST"])

if __name__ == "__main__":
    app.run()
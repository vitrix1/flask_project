from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Ads
from schema import CreateAd, VALIDATION_CLASS
from pydantic import ValidationError

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
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
        model_obj_dict = model_obj.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


def get_ad(session: Session, ad_id: int):
    ad = session.get(Ads, ad_id)
    if ad is None:
        raise HttpError(404, message="ad doesn't exist")
    return ad


class AdsView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(session, ad_id)
            return jsonify(
                {
                    "id": ad.id,
                    "header": ad.header,
                    "description": ad.description,
                    "owner": ad.owner,
                    "creation_time": ad.creation_time.isoformat(),
                }
            )

    def post(self):
        json_data = validate_json(request.json, CreateAd)
        with Session() as session:
            ad = Ads(**json_data)
            session.add(ad)
            session.commit()
            return jsonify({"id": ad.id})

    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return jsonify({"status": "success"})


app.add_url_rule(
    "/ad/<int:ad_id>",
    view_func=AdsView.as_view("with_ad_id"),
    methods=["GET", "DELETE"],
)

app.add_url_rule("/ad/", view_func=AdsView.as_view("create_ad"), methods=["POST"])

if __name__ == "__main__":
    app.run()

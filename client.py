import requests


def post():
    response = requests.post("http://127.0.0.1:5000/ad/",
                             json={
                                 "header": "Куплю гараж",
                                 "description": "Гараж в ОТС",
                                 "owner": "Виталя",
                             }
                             )
    print(response.json())


def get(ad_id):
    response = requests.get(f"http://127.0.0.1:5000/ad/{ad_id}", )
    print(response.json())


def delete(ad_id):
    response = requests.delete(f"http://127.0.0.1:5000/ad/{ad_id}",)
    print(response.json())


if __name__ == '__main__':
    post()
    # get(1)
    # delete(1)


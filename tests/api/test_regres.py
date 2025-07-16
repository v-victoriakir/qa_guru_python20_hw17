import requests
from jsonschema import validate

import schemas

url = 'https://reqres.in'
list_users_endpoint = '/api/users'
users_endpoint = '/api/users/'
register_endpoint = '/api/register'
unknown_endpoint = '/api/unknown/'


def test_list_users():
    params = {"page": 2}
    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.get(url + list_users_endpoint, params=params, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body["page"] == 2


def test_get_single_user():
    user_id = '2'
    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.get(url + users_endpoint + user_id, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body["data"]["email"] == "janet.weaver@reqres.in"
    assert body["data"]["first_name"] == "Janet"
    assert body["data"]["last_name"] == "Weaver"

    validate(body, schema=schemas.get_single_user)


def test_get_single_user_not_found():
    user_id = '23'
    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.get(url + unknown_endpoint + user_id, headers=headers)

    assert response.status_code == 404


def test_create_user():
    name = 'vicky'
    job = 'teacher'

    payload = {
        'name': name,
        'job': job
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.post(url + users_endpoint, json=payload, headers=headers)

    assert response.status_code == 201
    validate(response.json(), schema=schemas.create_user)


def test_update_user():
    name = 'vicky'
    job = 'teacher'
    user_id = '2'

    payload = {
        'name': name,
        'job': job
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.put(url + users_endpoint + user_id, json=payload, headers=headers)

    assert response.status_code == 200
    validate(response.json(), schema=schemas.update_user)


def test_delete_user():
    user_id = '2'
    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.delete(url + users_endpoint + user_id, headers=headers)

    assert response.status_code == 204


def test_register_user_success():
    email = 'eve.holt@reqres.in'
    password = 'pistol'

    payload = {
        'email': email,
        'password': password
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.post(url + register_endpoint, json=payload, headers=headers)

    assert response.status_code == 200
    validate(response.json(), schema=schemas.register_user)


def test_register_user_unsuccessful():
    password = 'pistol'

    payload = {
        'password': password
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.post(url + register_endpoint, json=payload, headers=headers)

    assert response.status_code == 400
    validate(response.json(), schema=schemas.register_unsuccessful)


def test_check_single_user_is_on_the_list():
    expected_user = {
        "id": 7,
        "email": "michael.lawson@reqres.in",
        "last_name": "Lawson"
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    params = {"page": 2}
    response = requests.get(url + list_users_endpoint, params=params, headers=headers)
    body = response.json()

    assert response.status_code == 200

    users = body.get('data', [])

    user_found = any(
        user.get("id") == expected_user["id"] and
        user.get("email") == expected_user["email"] and
        user.get("last_name") == expected_user["last_name"]
        for user in users
    )

    assert user_found

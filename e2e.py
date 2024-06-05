import requests
from faker import Faker

faker = Faker()

BASE_URL = "http://localhost:8000"


def register_user(username, password, email):
    url = f"{BASE_URL}/user/register"
    payload = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=payload)
    return response.json()


def login_user(username, password):
    url = f"{BASE_URL}/user/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, data=payload)
    return response.json()


def create_todo(token, title, description):
    url = f"{BASE_URL}/todo/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"title": title, "description": description}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_todos(token):
    url = f"{BASE_URL}/todo/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def update_todo(token, todo_id, title):
    url = f"{BASE_URL}/todo/{todo_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"title": title}
    response = requests.patch(url, json=payload, headers=headers)
    return response.json()


def delete_todo(token, todo_id):
    url = f"{BASE_URL}/todo/{todo_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return response.status_code


def create_task(token, title, description, todo_id):
    url = f"{BASE_URL}/task/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": title,
        "description": description,
        "todo_id": todo_id,
        "priority": 0,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_tasks(token):
    url = f"{BASE_URL}/task/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def update_task(token, task_id, title, description):
    url = f"{BASE_URL}/task/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"title": title, "description": description}
    response = requests.patch(url, json=payload, headers=headers)
    return response.json()


def delete_task(token, task_id):
    url = f"{BASE_URL}/task/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return response.status_code


def main():
    username = faker.user_name()
    password = faker.password()
    email = faker.email()
    description = faker.sentence(nb_words=41)

    # Register a new user
    register_response = register_user(username, password, email)
    print("Register Response:", register_response)

    # Login the user
    login_response = login_user(username, password)
    print("Login Response:", login_response)
    token = login_response.get("access_token")

    if not token:
        print("Failed to login. Exiting.")
        return

    todo_title = faker.sentence(nb_words=4)

    create_todo_response = create_todo(token, todo_title, description)
    print("Create Todo Response:", create_todo_response)
    todo_id = create_todo_response.get("id")

    if not todo_id:
        print("Failed to create Todo. Exiting.")
        return

    get_todos_response = get_todos(token)
    print("Get Todos Response:", get_todos_response)

    updated_title = faker.sentence(nb_words=4)

    update_todo_response = update_todo(token, todo_id, updated_title)
    print("Update Todo Response:", update_todo_response)

    task_title = faker.sentence(nb_words=4)
    task_description = faker.paragraph()

    create_task_response = create_task(token, task_title, task_description, todo_id)
    print("Create Task Response:", create_task_response)
    task_id = create_task_response.get("id")

    if not task_id:
        print("Failed to create Task. Exiting.")
        return

    get_tasks_response = get_tasks(token)
    print("Get Tasks Response:", get_tasks_response)

    updated_title = faker.sentence(nb_words=4)
    updated_description = faker.paragraph()

    update_task_response = update_task(
        token, task_id, updated_title, updated_description
    )
    print("Update Task Response:", update_task_response)

    delete_task_response = delete_task(token, task_id)
    print("Delete Task Response Status Code:", delete_task_response)
    delete_todo_response = delete_todo(token, todo_id)
    print("Delete Todo Response Status Code:", delete_todo_response)


if __name__ == "__main__":
    main()

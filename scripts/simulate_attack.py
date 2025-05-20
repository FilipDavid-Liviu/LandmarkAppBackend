import requests
import time
import random
from datetime import datetime

API_URL = "http://localhost:8000"
USERNAME = "test_user"
PASSWORD = "test_password"
LANDMARK_IDS = list(range(1, 21))
ITERATIONS = 30
DELAY = 0.1

def login():
    response = requests.post(
        f"{API_URL}/users/login/",
        data={"username": USERNAME, "password": PASSWORD}
    )
    if response.status_code == 200:
        print("Login successful")
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def register():
    response = requests.post(
        f"{API_URL}/users/register/",
        json={"username": USERNAME, "password": PASSWORD}
    )
    if response.status_code == 200:
        print("Registration successful")
    else:
        print(f"Registration failed: {response.status_code} - {response.text}")
        raise Exception("Failed to register user")

def save_landmark(token, landmark_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_URL}/saved_landmarks/save/{landmark_id}",
        headers=headers
    )
    if response.status_code != 200:
        print(f"Failed to save landmark {landmark_id}: {response.status_code} - {response.text}")

def unsave_landmark(token, landmark_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_URL}/saved_landmarks/unsave/{landmark_id}",
        headers=headers
    )
    if response.status_code != 200:
        print(f"Failed to unsave landmark {landmark_id}: {response.status_code} - {response.text}")

def simulate_attack():
    print("Starting attack simulation...")
    print(f"Time: {datetime.now()}")
    
    token = login()
    if not token:
        print("Attempting to register new user...")
        register()
        token = login()
        if not token:
            raise Exception("Login failed after registration, aborting.")

    print("\nSpamming save/unsave operations...")
    for i in range(ITERATIONS):
        landmark_id = random.choice(LANDMARK_IDS)
        
        save_landmark(token, landmark_id)
        print(f"[{i+1}/{ITERATIONS}] Saved landmark {landmark_id}")
        
        time.sleep(DELAY / 2)

        unsave_landmark(token, landmark_id)
        print(f"[{i+1}/{ITERATIONS}] Unsave landmark {landmark_id}")
        
        time.sleep(DELAY)

    print("\nAttack simulation completed!")
    print(f"Time: {datetime.now()}")
    print("\nCheck the admin dashboard to see if the user was flagged as suspicious.")

if __name__ == "__main__":
    simulate_attack()

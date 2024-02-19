import requests
import os
# Server URL
SERVER_URL = 'http://localhost:8005'


def list_files():
    # Send a GET request to list files
    response = requests.get(f"{SERVER_URL}/list_files")
    if response.status_code == 200:
        print("Files available on the server:")
        print(response.text)
    else:
        print(f"Failed to retrieve file list. Status code: {response.status_code}")


def download_file(file_name):
    # Send a GET request to download a file
    response = requests.get(f"{SERVER_URL}/{file_name}")
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"File '{file_name}' downloaded successfully")
    else:
        print(f"Failed to download file '{file_name}'. Status code: {response.status_code}")


def upload_file(file_path):
    try:
        # Extracting the filename from the file path
        file_name = os.path.basename(file_path)

        # Send a POST request to upload the file
        files = {'file': (file_name, open(file_path, 'rb'))}
        response = requests.post(f"{SERVER_URL}/{file_name}", files=files)

        if response.status_code == 200:
            print(f"File '{file_path}' uploaded successfully")
        else:
            print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while uploading file '{file_path}': {e}")


def main():
    while True:
        print("1. List files\n2. Download file\n3. Upload file \n4.Exit")
        choice = input("Enter your choice: ")

        if choice.isdigit():  # Check if the input is a valid integer
            choice = int(choice)
            if choice == 1:
                list_files()
            elif choice == 2:
                file_name = input("Enter the name of the file to download: ")
                download_file(file_name)
            elif choice == 3:
                file_path = input("Enter the path of the file to upload: ")
                upload_file(file_path)
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please enter a valid option.")
        else:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()

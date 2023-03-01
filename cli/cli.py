import argparse
import os
import requests

PLATFORM_API_BASE_URL = os.environ.get("PLATFORM_API_BASE_URL", "http://127.0.0.1:80/")


def get_auth_token():
    command = "gcloud auth print-identity-token"
    result = os.popen(command).read().strip()
    return result


def access_bucket(bucket_name):
    url = f"{PLATFORM_API_BASE_URL}/request_access_for_bucket?bucket={bucket_name}"
    headers = {"Authorization": f"Bearer {get_auth_token()}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(
            f"Failed to get objects from {bucket_name}. Status code: {response.status_code}"
        )


def main():
    parser = argparse.ArgumentParser(
        prog="""
.______    __          ___   .___________. _______   ______   .______      .___  ___.      ______  __       __  
|   _  \  |  |        /   \  |           ||   ____| /  __  \  |   _  \     |   \/   |     /      ||  |     |  | 
|  |_)  | |  |       /  ^  \ `---|  |----`|  |__   |  |  |  | |  |_)  |    |  \  /  |    |  ,----'|  |     |  | 
|   ___/  |  |      /  /_\  \    |  |     |   __|  |  |  |  | |      /     |  |\/|  |    |  |     |  |     |  | 
|  |      |  `----./  _____  \   |  |     |  |     |  `--'  | |  |\  \----.|  |  |  |    |  `----.|  `----.|  | 
| _|      |_______/__/     \__\  |__|     |__|      \______/  | _| `._____||__|  |__|     \______||_______||__| 
                                                                                                                
        """,
        description="Request access to Google Cloud Storage bucket",
        epilog="cool",
    )
    parser.add_argument(
        "--bucket-name", help="Name of the bucket get access to", required=True
    )
    args = parser.parse_args()
    access_bucket(args.bucket_name)


if __name__ == "__main__":
    main()

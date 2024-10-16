from typing_extensions import Annotated

import typer

from kubiya_sdk.tools import function_tool


@function_tool(
    description="Prints pandas {name}!",
    requirements=["pandas==2.2.3"],
)
def test_123(
    name: str,
    boolean_val: bool,  # This will validate that the input is a boolean
    optional_str: Annotated[
        str, typer.Argument()
    ] = "sheeesh",  # This is how to add a default value
):
    import pandas as pd

    print(f"Hello {name}! {boolean_val} {optional_str}")
    df = pd.DataFrame(
        {"name": [name], "boolean_val": [boolean_val], "test": [optional_str]}
    )

    print(df)

@function_tool(
    description="Image vision analyzer!",
    requirements=["litellm"],
    env=["LLM_KEY", "LLM_BASE_URL"],
)
def image_vision_analyzer():
    import os
    from litellm import completion

    llm_key = os.getenv("LLM_KEY")
    llm_base_url = os.getenv("LLM_BASE_URL")

    # openai call
    response = completion(
        model="openai/gpt-4o",
        api_key=llm_key,
        base_url=llm_base_url,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                        },
                    },
                ],
            }
        ],
    )

    print(response.choices[0].message.content)


@function_tool(
    description="Prints pandas {name}!",
    requirements=["pandas==2.2.3", "requests==2.25.1"],
    env=["ARGOCD_SERVER", "ARGOCD_USERNAME", "ARGOCD_PASSWORD"],
)
def list_argo_apps():
    import os
    import requests

    ARGOCD_SERVER = os.getenv('ARGOCD_SERVER')
    ARGOCD_USERNAME = os.getenv('ARGOCD_USERNAME')
    ARGOCD_PASSWORD = os.getenv('ARGOCD_PASSWORD')

    if not ARGOCD_SERVER or not ARGOCD_USERNAME or not ARGOCD_PASSWORD:
        print("Missing environment variables.")
        return

    # Ensure the server URL starts with https://
    if not ARGOCD_SERVER.startswith("http://") and not ARGOCD_SERVER.startswith("https://"):
        ARGOCD_SERVER = "https://" + ARGOCD_SERVER

    # Login to Argo CD to obtain a token
    try:
        response = requests.post(
            f"{ARGOCD_SERVER}/api/v1/session",
            json={"username": ARGOCD_USERNAME, "password": ARGOCD_PASSWORD},
            verify=False  # Skip SSL verification
        )
        response.raise_for_status()
        token = response.json()['token']
    except Exception as e:
        print(f"Failed to login: {e}")
        return

    # Get the list of applications
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f"{ARGOCD_SERVER}/api/v1/applications",
            headers=headers,
            verify=False  # Skip SSL verification
        )
        response.raise_for_status()
        apps = response.json()['items']
        for app in apps:
            print(app['metadata']['name'])
    except Exception as e:
        print(f"Failed to retrieve applications: {e}")



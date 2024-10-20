from . import main

import inspect

from . import grafana

from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry



image_vision = Tool(
    name="image_vision",
    type="docker",
    image="python:3.12",
    description="Image Vision!",
    args=[],
    content="""
curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env

uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1

uv pip install -r /tmp/requirements.txt > /dev/null 2>&1

python /tmp/main.py
""",
    with_files=[
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
        FileSpec(
            destination="/tmp/requirements.txt",
            content="requests",
        ),
    ],
)


get_grafana_image_and_send_slack_thread = Tool(
    name="get_grafana_image_and_send_slack_thread",
    description="Generate render URLs for relevant Grafana dashboard panels, download images, analyze them using OpenAI's vision model, and send results to the current Slack thread",
    type="docker",
    image="python:3.11-bullseye",
    content="""
pip install slack_sdk requests==2.32.3 litellm==1.49.5 pillow==11.0.0 > /dev/null 2>&1

python /tmp/grafana.py --grafana_dashboard_url "$grafana_dashboard_url" --alert_subject "$alert_subject"
""",
    secrets=[
        "SLACK_API_TOKEN",
        "GRAFANA_API_KEY",
        "VISION_LLM_KEY"
    ],
    env=[
        "SLACK_THREAD_TS",
        "SLACK_CHANNEL_ID",
        "VISION_LLM_BASE_URL"
    ],
    args=[
        Arg(
            name="grafana_dashboard_url",
            type="str",
            description="URL of the Grafana dashboard",
            required=True
        ),
        Arg(
            name="alert_subject",
            type="str",
            description="Subject of the alert, used to filter relevant panels",
            required=True
        )
    ],
    with_files=[
        FileSpec(
            destination="/tmp/grafana.py",
            source=inspect.getsource(grafana),
        ),
        FileSpec(
            destination="/tmp/requirements.txt",
            content="""slack_sdk==3.11.0\nrequests==2.32.3\nlitellm==1.49.5\npillow==11.0.0""",
        ),
    ],
    dependencies=["slack_sdk", "requests", "litellm", "pillow"]
)

# Register the updated tool
tool_registry.register("freshworks", get_grafana_image_and_send_slack_thread)
tool_registry.register("image_vision", image_vision)

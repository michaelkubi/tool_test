import inspect

from kubiya_sdk.tools.models import Arg, Tool, FileSpec, ImageProvider, Auth
from kubiya_sdk.tools.registry import tool_registry

from . import main

hello_tool = Tool(
    name="say_hello",
    type="docker",
    image="dmichaelb/test:amd",
    description="Prints hello {name}!",
    args=[Arg(name="name", description="name to say hello to", required=True)],
    image_provider=ImageProvider(
        kind="dockerhub",
        auth=[
            Auth(name="username", value="dmichaelb"), 
            Auth(name="password", value_from={"secret": "MICHAEL_DH_PASSWORD"})
        ],
    ),
    on_build="""
curl -LsSf https://astral.sh/uv/0.4.27/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env

uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1

if [ -f /tmp/requirements.txt ]; then
    uv pip install -r /tmp/requirements.txt > /dev/null 2>&1
fi
""",
    content="""
python /tmp/main.py $name
""",
    with_files=[
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
    secrets=["MICHAEL_DH_PASSWORD"],
)

tool_registry.register("hello_world_tool", hello_tool)

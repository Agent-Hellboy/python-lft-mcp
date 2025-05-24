from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import os
import glob
import asyncio
import logging

mcp = FastMCP(
    name="python-lft",
    dependencies=["ruff", "black", "pytest", "fastapi"],
    # JSON‐only on the HTTP mount:
    stateless_http=True,
    json_response=True,
)

app = FastAPI(title="Python LFT Server")

#  Mount MCP SSE under /sse for the Inspector
app.mount("/sse", mcp.sse_app())

#  Mount Streamable-HTTP under /mcp for JSON clients
app.mount("/mcp", mcp.streamable_http_app())

# Your own health check
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@mcp.tool(name="lint", description="Run ruff lint")
async def lint(target: str = "all") -> str:
    logging.info(f"Linting {target}")
    if target == "all":
        files = [
            f for f in glob.glob("**/*.py", recursive=True)
            if f.endswith(".py")
        ]
    else:
        files = [target]


    out = []
    for f in files:
        proc = await asyncio.create_subprocess_exec(
            "ruff", "check", f, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        s, e = await proc.communicate()
        out.append((s or e).decode())
    return "".join(out)

@mcp.tool(name="format", description="Run black formatter")
async def format_code(target: str = "all", line_length: int = 88) -> str:
    logging.info(f"Formatting {target}")
    files = glob.glob("**/*.py", recursive=True) if target == "all" else [target]
    out = []
    for f in files:
        proc = await asyncio.create_subprocess_exec(
            "black", "--line-length", str(line_length), f,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        s, e = await proc.communicate()
        out.append((s or e).decode())
    return "".join(out)

@mcp.tool(name="test", description="Run pytest")
async def test(target: str = "all") -> str:
    args = ["pytest", "--maxfail=1", "--disable-warnings"]
    if target != "all":
        args.append(target)
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    s, e = await proc.communicate()
    return (s + e).decode()

@mcp.tool(name="check_config_files", description="Check for common config files")
async def check_config_files() -> dict:
    return {
        cfg: os.path.exists(cfg)
        for cfg in ("pyproject.toml", "pytest.ini", ".ruff.toml")
    }

if __name__ == "__main__":
    mcp.run()

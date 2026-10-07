from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.mcp_server import mcp
from app.tools.dictionary import register_dictionary_tools


# Register MCP tools
register_dictionary_tools(mcp)


# Create MCP ASGI application
mcp_app = mcp.streamable_http_app()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:

    async with mcp.session_manager.run():
        yield


app = FastAPI(
    title="MoneySense MCP",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "moneysense-mcp",
        "version": "0.1.0",
    }


@app.get("/")
async def root():

    return {
        "name": "MoneySense",
        "description": "Financial literacy MCP server",
        "mcp": "/mcp",
    }


# Mount MCP AFTER ordinary FastAPI routes
app.mount("/", mcp_app)
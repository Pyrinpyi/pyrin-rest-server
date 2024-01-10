# encoding: utf-8
from typing import List

from pydantic import BaseModel

from server import app, pyrin_client


class BlockdagResponse(BaseModel):
    blueScore: int = 260890


@app.get("/info/virtual-chain-blue-score", response_model=BlockdagResponse, tags=["Pyrin network info"])
async def get_virtual_selected_parent_blue_score():
    """
    Returns the blue score of virtual selected parent
    """
    resp = await pyrin_client.request("getVirtualSelectedParentBlueScoreRequest")
    return resp["getVirtualSelectedParentBlueScoreResponse"]

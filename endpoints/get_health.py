# encoding: utf-8
import hashlib
from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from dbsession import async_session
from models.Transaction import Transaction
from server import app, pyrin_client


class PyipadResponse(BaseModel):
    pyrinHost: str = ""
    serverVersion: str = "0.12.6"
    isUtxoIndexed: bool = True
    isSynced: bool = True
    p2pId: str = "1231312"


class HealthResponse(BaseModel):
    pyrinServers: List[PyipadResponse]


@app.get("/info/health", response_model=HealthResponse, tags=["Pyrin network info"])
async def health_state():
    """
    Returns the current hashrate for Pyrin network in TH/s.
    """
    await pyrin_client.initialize_all()

    pyrins = []

    async with async_session() as s:
        last_block_time = (await s.execute(select(Transaction.block_time)
                                           .limit(1)
                                           .order_by(Transaction.block_time.desc()))).scalar()

    time_diff = datetime.now() - datetime.fromtimestamp(last_block_time / 1000)

    if time_diff > timedelta(minutes=10):
        raise HTTPException(status_code=500, detail="Transactions not up to date")

    for i, pyrin_info in enumerate(pyrin_client.pyrins):
        pyrins.append({
            "isSynced": pyrin_info.is_synced,
            "isUtxoIndexed": pyrin_info.is_utxo_indexed,
            "p2pId": hashlib.sha256(pyrin_info.p2p_id.encode()).hexdigest(),
            "pyrinHost": f"PYIPAD_HOST_{i + 1}",
            "serverVersion": pyrin_info.server_version
        })

    return {
        "pyrinServers": pyrins
    }

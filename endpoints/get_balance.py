# encoding: utf-8

from fastapi import Path, HTTPException
from pydantic import BaseModel

from server import app, pyrin_client


class BalanceResponse(BaseModel):
    address: str = "pyrin:qqpz0ndsjsmlaxmcp33mqrx263dn4n8x9y67gysfkgws8kqa0w9szz6mzdhcq"
    balance: int = 38240000000


@app.get("/addresses/{pyrinAddress}/balance", response_model=BalanceResponse, tags=["Pyrin addresses"])
async def get_balance_from_pyrin_address(
        pyrinAddress: str = Path(
            description="Pyrin address as string e.g. pyrin:qqpz0ndsjsmlaxmcp33mqrx263dn4n8x9y67gysfkgws8kqa0w9szz6mzdhcq",
            regex="^pyrin(?:test)?\:[a-z0-9]{61,63}$")):
    """
    Get balance for a given pyrin address
    """
    resp = await pyrin_client.request("getBalanceByAddressRequest",
                                       params={
                                           "address": pyrinAddress
                                       })

    try:
        resp = resp["getBalanceByAddressResponse"]
    except KeyError:
        if "getUtxosByAddressesResponse" in resp and "error" in resp["getUtxosByAddressesResponse"]:
            raise HTTPException(status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"])
        else:
            raise

    try:
        balance = int(resp["balance"])

    # return 0 if address is ok, but no utxos there
    except KeyError:
        balance = 0

    return {
        "address": pyrinAddress,
        "balance": balance
    }

# encoding: utf-8

from pydantic import BaseModel

from endpoints import sql_db_only
from server import app, pyrin_client
from fastapi.responses import PlainTextResponse


class CoinSupplyResponse(BaseModel):
    circulatingSupply: str = "0"
    maxSupply: str = "[100000000000000000]"


@app.get("/info/coinsupply", response_model=CoinSupplyResponse, tags=["Pyrin network info"])
async def get_coinsupply():
    """
    Get $PYI coin supply information
    """
    resp = await pyrin_client.request("getCoinSupplyRequest")
    print(resp)
    return {
        "circulatingSupply": resp["getCoinSupplyResponse"]["circulatingLeor"],
        "totalSupply": resp["getCoinSupplyResponse"]["circulatingLeor"],
        "maxSupply": resp["getCoinSupplyResponse"]["maxLeor"]
    }

@app.get("/info/coinsupply/circulating", tags=["Pyrin network info"],
         response_class=PlainTextResponse)
async def get_circulating_coins(in_billion : bool = False):
    """
    Get circulating amount of $PYI token as numerical value
    """
    resp = await pyrin_client.request("getCoinSupplyRequest")
    coins = str(float(resp["getCoinSupplyResponse"]["circulatingLeor"]) / 100000000)
    if in_billion:
        return str(round(float(coins) / 1000000000, 2))
    else:
        return coins


@app.get("/info/coinsupply/total", tags=["Pyrin network info"],
         response_class=PlainTextResponse)
async def get_total_coins():
    """
    Get total amount of $PYI token as numerical value
    """
    resp = await pyrin_client.request("getCoinSupplyRequest")
    return str(float(resp["getCoinSupplyResponse"]["circulatingLeor"]) / 100000000)

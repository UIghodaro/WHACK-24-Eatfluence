from typing import Any, Dict, List, Optional
from uagents import Agent, Context, Model, Bureau
from uagents.setup import fund_agent_if_low
import time

class GeolocationRequest(Model):
    address: str

class GeolocationResponse(Model):
    latitude: float
    longitude: float

class Coordinates(Model):
    latitude: float
    longitude: float


class POIAreaRequest(Model):
    loc_search: Coordinates
    radius_in_m: int
    limit: int = 20
    query_string: str
    filter: Dict[str, Any] = {}


class POI(Model):
    placekey: str
    location_name: str
    brands: Optional[List[str]] = None
    top_category: Optional[str] = None
    sub_category: Optional[str] = None
    location: Coordinates
    address: str
    city: str
    region: Optional[str] = None
    postal_code: str
    iso_country_code: str
    metadata: Optional[Dict[str, Any]] = None


class POIResponse(Model):
    loc_search: Coordinates
    radius_in_m: int
    data_origin: str
    data: List[POI]

class Request(Model):
    text: str
 
class Response(Model):
    timestamp: int
    text: str
    agent_address: str

AGENT_MAILBOX_KEY_GEO = "25eb6f8b-7a5b-448e-b88d-b3104156f5f8"
geo_agent = Agent(
    name="user",
    seed = 'geolocation seed 2024 again',
    mailbox=f"{AGENT_MAILBOX_KEY_GEO}@https://agentverse.ai",
    port = 8001
)

AGENT_MAILBOX_KEY_POI = ""
poi_agent = Agent(
    name="user",
    seed = 'user for luis whack 2024 v2222',
    mailbox=f"{AGENT_MAILBOX_KEY_POI}@https://agentverse.ai",
    port = 8002
)

crazy_address = "University of Warwick, Coventry"

AI_AGENT_ADDRESS = "agent1qvnpu46exfw4jazkhwxdqpq48kcdg0u0ak3mz36yg93ej06xntklsxcwplc"
@geo_agent.on_event("startup")
async def send_message(ctx: Context):
    ctx.logger.info(f"Sent address to Geolocation agent: {crazy_address}")
    await ctx.send(AI_AGENT_ADDRESS, GeolocationRequest(address=crazy_address))

@geo_agent.on_rest_get("/rest/get", Response)
async def handle_get(ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("Received GET request")
    return {
        "timestamp": int(time.time()),
        "text": "Hello from the GET handler!",
        "agent_address": ctx.agent.address,
    }
 
@geo_agent.on_rest_post("/rest/post", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    ctx.logger.info("Received POST request")
    return Response(
        text=f"Received: {req.text}",
        agent_address=ctx.agent.address,
        timestamp=int(time.time()),
    )
    

GOOGLE_MAPS_POI_AGENT_ADDRESS = "agent1qwf6cn80p4q97pw57g0elzf6d4jrg8jfkmafu6z6jhjwurdganw7u0m865e"
@geo_agent.on_message(model=GeolocationResponse)
async def handle_response(ctx: Context, sender: str, msg: GeolocationResponse):
    # ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")
    
    await ctx.send(GOOGLE_MAPS_POI_AGENT_ADDRESS, GeolocationResponse(latitude = msg.latitude, longitude = msg.longitude))

example_request = POIAreaRequest(
    loc_search=Coordinates(latitude=48.140505822096365, longitude=11.559987118245475),
    radius_in_m=500,
    query_string="coffee shop",
)

GMAPS_AGENT_ADDRESS = "agent1qwf6cn80p4q97pw57g0elzf6d4jrg8jfkmafu6z6jhjwurdganw7u0m865e"
@poi_agent.on_message(model = GeolocationResponse)
async def message_handler(ctx: Context, sender : str, msg: GeolocationResponse):
    ctx.logger.info(f'Recieved message from {sender} : {msg.latitude} , {msg.longitude}')

    await ctx.send(GMAPS_AGENT_ADDRESS, example_request)


# @poi_agent.on_event("startup")
# async def handle_startup(ctx: Context):
#     await ctx.send(GMAPS_AGENT_ADDRESS, example_request)
#     ctx.logger.info(f"Sent request to  agent: {example_request}")


@poi_agent.on_message(POIResponse)
async def handle_response(ctx: Context, sender: str, msg: POIResponse):
    ctx.logger.info(f"Received {len(msg.data)} pois from: {sender}")
    for place in msg.data:
        ctx.logger.info(place.location_name)
    
    # for n in nearby_places:
    #     name_score = trend_scraper.analyse_food_relation(n)
    #     print("Name score: " + str(name_score))

    #     restaurant_name = n
    #     if name_score < 0.45:
    #         restaurant_name = restaurant_name + " Restaurant"

    #     print("Scraping " + str(restaurant_name))
    #     trend_scraper.tiktok_scrape(restaurant_name)

bureau = Bureau()
bureau.add(geo_agent)
bureau.add(poi_agent)

if __name__ == "__main__":
    bureau.run()


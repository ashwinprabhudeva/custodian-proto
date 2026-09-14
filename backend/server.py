from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class BookingCreate(BaseModel):
    experience_id: str
    date: str
    guests: int = Field(default=1, ge=1, le=20)

class LegacyCreate(BaseModel):
    experience_id: str
    text: str

EXPERIENCES = [
    {"id":"yakshagana","title":"An evening inside Yakshagana","category":"Performance","region":"Udupi","custodian":"Raghav Bhandary","role":"Yakshagana performer","image":"https://images.unsplash.com/photo-1707344238570-04d1d233090c?q=85&w=1000&auto=format&fit=crop","tone":"terracotta","price":"Donation-based","price_note":"₹400 suggested","cap":"Capped at 15 people","policy":"No close-up photography during sequences","participation":"Watch-only","season":"Available most evenings","verified":"Udupi Yakshagana Kala Kendra","boosted":True,"description":"I grew up backstage, folding costumes and listening for the chende to begin. Come sit close enough to feel the rhythm, but give the performers the space the story needs.","review":"The moment the drums started, the whole room changed. Raghav made us feel like guests, not an audience.","reviewer":"Maya, Bengaluru","bio":"Third-generation performer and keeper of a small rehearsal space near Manipal.","legacy":["Which character should a first-time visitor watch for?","What does the red face paint mean in this story?"]},
    {"id":"coffee","title":"A proper Udupi meal on a banana leaf","category":"Food","region":"Manipal","custodian":"Anitha Pai","role":"Home cook & coffee host","image":"https://static.prod-images.emergentagent.com/jobs/3514529a-2e4d-44e7-ac68-03f047d59898/images/e3b15b876b6402da80b2f640499e0fb405532756326711df31f9ea6e2992476e.jpeg","tone":"moss","price":"Fixed price","price_note":"₹1,400 per person","cap":"Small group: 2–4","policy":"Please ask before photographing our home","participation":"Hands-on","season":"Available year-round","verified":"Coastal Foodways Collective","boosted":True,"description":"We will eat the way my family eats on a good Sunday: rice, sambar, vegetables, kosambari, payasam, and coffee poured high from the steel davara. Come hungry and sit close to the kitchen.","review":"The banana leaf meal felt like being welcomed into a real Sunday, not attending a demonstration.","reviewer":"Arjun, Mumbai","bio":"Anitha hosts from her family home, sharing a full Udupi-style vegetarian meal and the small rituals around it.","legacy":["Ask about the brass filter — it has a story."]},
    {"id":"ritual","title":"Before the town wakes","category":"Ritual / Religious","region":"Udupi","custodian":"Suresh Acharya","role":"Ritual custodian","image":"https://static.prod-images.emergentagent.com/jobs/3514529a-2e4d-44e7-ac68-03f047d59898/images/fe59b9c4b21333c362bced9865e12197ebddfcec814eb316eca7d09ef7766dfb.jpeg","tone":"ochre","price":"Donation-based","price_note":"Suggested ₹250","cap":"Capped access: 8","policy":"Audio recording only; no flash","participation":"Watch-only","season":"Early mornings, by request","verified":"Udupi Heritage Circle","boosted":False,"description":"The quiet before the first bell is what I want you to notice. This is a viewing, not a performance. I will show you where to stand and when to lower your voice.","review":"A gentle, respectful introduction to a place I thought I already knew.","reviewer":"Leela, Chennai","bio":"Suresh helps visitors understand the rhythm and boundaries of a fictionalized Krishna Matha-style ritual space.","legacy":["Leave room for the silence." ]},
    {"id":"fishing","title":"Read the tide at Malpe","category":"Nature / Fishing","region":"Udupi","custodian":"Mohan Saldanha","role":"Coastal fisherman","image":"https://images.unsplash.com/photo-1708880816742-d1b07543fbea?q=85&w=1000&auto=format&fit=crop","tone":"sea","price":"Fixed price","price_note":"₹900 per person","cap":"Group size: 2–3","policy":"No photos of other boats without asking","participation":"Hands-on","season":"Tide-timed: 5:30–8:00am","verified":"Malpe Coastal Commons","boosted":False,"description":"The sea tells us when to leave. We will check the tide, pull the small net, and come back before the sun gets too high. Bring a hat, not a schedule.","review":"Mohan taught us to look at the water before looking at the clock.","reviewer":"Tomas, Berlin","bio":"Mohan fishes the Malpe coast with his brother and teaches visitors to read its changing edges.","legacy":["Wear sandals you can rinse clean."]},
    {"id":"coir","title":"Hands in coir","category":"Craft","region":"Manipal","custodian":"Janaki Kotian","role":"Coir & handicraft artisan","image":"https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d?q=85&w=1000&auto=format&fit=crop","tone":"gold","price":"Negotiable","price_note":"Agree together","cap":"Flexible group size","policy":"Patterns are IP-protected; no copying or commercial use","participation":"Hands-on","season":"Available Tue–Sat","verified":"Karnataka Craft Guild","boosted":False,"description":"Coir has a stubbornness to it. It teaches your hands to slow down. I will show you one weave from my family’s practice, but the pattern stays here.","review":"The most satisfying two hours of our trip. Janaki was clear about what could be shared.","reviewer":"Nikhil, Pune","bio":"Janaki works with coconut fibre and protects the patterns passed through her family.","legacy":["Ask her how the fibre is softened before you begin."]},
    {"id":"kambala","title":"Weather the Kambala season","category":"Nature / Fishing","region":"Udupi","custodian":"Prakash Shetty","role":"Kambala farmer & trainer","image":"https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?q=85&w=1000&auto=format&fit=crop","tone":"indigo","price":"Fixed price","price_note":"₹1,000 per person","cap":"Capped at 10 people","policy":"No drones; keep a clear distance","participation":"Watch-only","season":"Only during Kambala season, Nov–Feb","verified":"Coastal Living Archive","boosted":True,"description":"The race is one day; the work is all year. I can show you how we care for the buffaloes and why the field is prepared the way it is. During the season only.","review":"We came for the race and left understanding the care behind it.","reviewer":"Sara, Kochi","bio":"Prakash trains Kambala buffaloes and opens a small window into the season around the race.","legacy":["The mud is part of the story, not a backdrop."]}
]

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Custodian API ready"}

@api_router.get("/experiences")
async def get_experiences(category: Optional[str] = None):
    return [e for e in EXPERIENCES if not category or category == "All" or e["category"] == category]

@api_router.get("/experiences/{experience_id}")
async def get_experience(experience_id: str):
    experience = next((e for e in EXPERIENCES if e["id"] == experience_id), None)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

@api_router.post("/bookings")
async def create_booking(input: BookingCreate):
    experience = next((e for e in EXPERIENCES if e["id"] == input.experience_id), None)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"id": str(uuid.uuid4()), "status":"pending_confirmation", "experience":experience["title"], "date":input.date, "guests":input.guests, "amount":experience["price_note"]}

@api_router.post("/legacy")
async def create_legacy(input: LegacyCreate):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Reflection cannot be empty")
    return {"id": str(uuid.uuid4()), "experience_id": input.experience_id, "text": input.text, "status":"visible_to_future_visitors"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
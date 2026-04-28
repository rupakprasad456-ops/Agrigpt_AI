from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from farmer_agent import FarmerAgent
from typing import List

app = FastAPI(title="AgriGPT Farmer Agent", description="AI assistant for farmers with pest and government scheme information")

class ChatRequest(BaseModel):
    chatId: str
    phone_number: str
    message: str
    api_key: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str]

class PestQuery(BaseModel):
    query: str

class PestResponse(BaseModel):
    pest: str
    details: str

class SchemeQuery(BaseModel):
    query: str

class SchemeResponse(BaseModel):
    scheme: str
    details: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint that intelligently routes to pest or scheme tools"""
    try:
        agent = FarmerAgent(api_key=request.api_key)
        result = agent.chat(
            message=request.message,
            chat_id=request.chatId,
            phone_number=request.phone_number
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/pests", response_model=PestResponse)
async def pests_endpoint(query: PestQuery):
    """Direct endpoint for pest and disease information"""
    try:
        # For this endpoint, we need an API key. In a real implementation,
        # this might come from headers or be optional
        agent = FarmerAgent(api_key="dummy_key")  # This endpoint doesn't use LLM
        result = agent.get_pest_info(query.query)
        return PestResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving pest information: {str(e)}")

@app.post("/schemes", response_model=SchemeResponse)
async def schemes_endpoint(query: SchemeQuery):
    """Direct endpoint for government scheme information"""
    try:
        # For this endpoint, we need an API key. In a real implementation,
        # this might come from headers or be optional
        agent = FarmerAgent(api_key="dummy_key")  # This endpoint doesn't use LLM
        result = agent.get_scheme_info(query.query)
        return SchemeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving scheme information: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AgriGPT Farmer Agent API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

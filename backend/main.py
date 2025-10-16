from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest
from pdf_loader import load_pdf
from ai_service import stream_response
import traceback

app = FastAPI(title="Chatbot PDF Reader")

# Enable CORS (update allowed origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to load PDF context at startup
try:
    pdf_context = load_pdf("Accessible_Travel_Guide_Partial.pdf")
except FileNotFoundError as e:
    pdf_context = None
    print(f"[Startup Error] {e}")

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chatbot endpoint with validations and proper error handling"""

    # Validate PDF availability
    if pdf_context is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF context could not be loaded. Please check the file path or server logs.",
        )

    # Validate user message
    user_message = request.message.strip() if request.message else ""
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'message' field cannot be empty.",
        )

    async def event_generator():
        try:
            async for token in stream_response(user_message, pdf_context):
                yield f"data: {token}\n\n"
        except Exception as e:
            print(f"[Streaming Error] {e}")
            traceback.print_exc()
            # Return a structured error to the client via SSE
            yield f'data: {{"type": "error", "content": "Internal server error: {str(e)}"}}\n\n'
            yield "data: {\"type\": \"done\"}\n\n"

    try:
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Chat Endpoint Error] {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request.",
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles known HTTP exceptions and returns clean JSON"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": exc.status_code},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handles unexpected exceptions"""
    print(f"[Unhandled Exception] {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "An unexpected error occurred on the server.",
            "details": str(exc),
        },
    )

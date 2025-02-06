# imports
import logging
import os
import requests

# Third party imports
from fastapi import FastAPI, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from prompts import DEFAULT_PROMPT

# local imports
from logging_config import setup_logging

load_dotenv()

# local imports

app = FastAPI(
    title="Realtime AI",
    description="Realtime AI API",
    version="1.0.0",
    debug=bool(int(os.getenv("DEBUG", False)))
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# logger setup
setup_logging()
logger = logging.getLogger()

# Open AI config
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")
openai_session_url = os.getenv("OPENAI_SESSION_URL")
openai_realtime_voice = os.getenv("OPENAI_REALTIME_VOICE")
openai_realtime_model = os.getenv("OPENAI_REALTIME_MODEL")


@app.post("/", include_in_schema=False)
def health_check():
    """
    Health check endpoint.

    Returns:
        str: "OK"
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "ok"})


@app.post("/rtc/connect")
async def connect_rtc_session(
    request: Request
):
    """
    Connect to a Realtime AI session.

    Returns:
        str: "OK"
    """
    try:
        # First Receive the client SDP from request
        sdp = await request.body()
        if not sdp:
            logger.error("SDP not received via request body.")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"success": False, "message": "SDP not received via request body", "error": "SDP not received via request body."})

        logger.info("SDP received via request body. %s", sdp)

        # Create Token header and payload to create ephemeral session
        ephemeral_headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }

        ephemeral_payload = {
            "model": openai_realtime_model,
            "voice": openai_realtime_voice
        }
        ephemeral_response = requests.post(
            url=openai_session_url, headers=ephemeral_headers, json=ephemeral_payload)

        if not ephemeral_response.ok:
            logger.error(
                "Error while creating ephemeral session. %s", ephemeral_response.text)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Error while creating ephemeral session",
                    "error": ephemeral_response.text
                }
            )
        token_data = ephemeral_response.json()
        ephemeral_token = token_data.get('client_secret', {}).get('value', '')
        if not ephemeral_token:
            logger.error(
                "Ephemeral Token not found.")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Ephemeral Token not found",
                    "error": "Ephemeral Token not found"
                }
            )
        # Sdp exchange with OPENAI
        sdp_headers = {
            "Authorization": f"Bearer {ephemeral_token}",
            "Content-Type": "application/sdp"
        }
        sdp_params = {
            "model": openai_realtime_model,
            "instructions": DEFAULT_PROMPT,
            "voice": openai_realtime_voice
        }
        sdp_url = requests.Request(
            "POST", openai_base_url, params=sdp_params).prepare().url
        sdp_response = requests.post(
            url=sdp_url, headers=sdp_headers, data=sdp)
        if not sdp_response.ok:
            logger.error(
                "Error while connecting to Realtime AI session. %s", sdp_response.text)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Error while connecting to Realtime AI session",
                    "error": sdp_response.text
                }
            )

        return Response(
            status_code=status.HTTP_200_OK,
            content=sdp_response.content,
            media_type="application/sdp"
        )

    except Exception as e:
        logger.info("Error connecting to Realtime AI session %s", e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Error connecting to Realtime AI session"})

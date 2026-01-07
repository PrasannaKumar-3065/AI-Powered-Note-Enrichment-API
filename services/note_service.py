import httpx
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note
from app.schemas.note import CreateNotes
import logging
from openai import AsyncOpenAI
from google import genai

logger = logging.getLogger(__name__)

class SummaryService:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
        self.settings = settings

    async def generate_summary(self, content: str) -> str:
        try:
            if len(content.split()) > settings.MAX_TOKENS:
                logger.warning(f"Summary API Token limit exceeded | limit {settings.MAX_TOKENS} input {len(content.split())}")
                return "Summary API Token limit exceeded"
            try:
                response = await AsyncOpenAI(api_key=settings.OPENAI_API_KEY).chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[{"role": "user", "content": content}],
                    max_tokens=settings.MAX_TOKENS
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"OpenAI API failed ({type(e).__name__}): {e}. Falling back to Gemini")
                try:
                    client = genai.Client(api_key=settings.GEMINI_API_KEY)
                    response = await client.aio.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=content
                    )
                    return response.text
                except Exception as gemini_error:
                    logger.warning(f"Gemini fallback failed: {gemini_error}")
                    return "Summary unavailable (all fallbacks failed)"
        except Exception as e:
            logger.exception(f"Unexpected error in summary service: {e}")
            return "Summary unavailable (unexpected error)"

class NoteService:
    def __init__(self, http_client: httpx.AsyncClient, repository):
        self.http_client = http_client
        self.repository = repository
    
    async def create_notes(self, session:AsyncSession, 
        note_data: CreateNotes, 
        summary_service: SummaryService
    ):
        summary = await summary_service.generate_summary(note_data.content)
        note_instance = Note(**dict(note_data), ai_summary=summary)
        return await self.repository.create_notes(session, note_instance)
    
    async def update_note(self, session:AsyncSession,note_id: str, 
        note_data: CreateNotes, 
        summary_service: SummaryService
    ):
        summary = await summary_service.generate_summary(note_data.content)
        note_instance = Note(**dict(note_data), ai_summary=summary)
        return await self.repository.update_notes(session, note_id, note_instance, summary)
    
    async def delete_notes(self, session:AsyncSession,note_id: str):
        return await self.repository.delete_notes(session, note_id)
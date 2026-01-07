from app.core.database import get_database_session
from app.repositories import note_repo
from app.schemas.note import CreateNotes, GetNotes, UpdateNotes
from app.services.note_service import SummaryService, NoteService
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

router = APIRouter(prefix="/notes", tags=["Notes"])

async def get_http_client() -> httpx.AsyncClient:
    from app.main import app
    if not hasattr(app.state, 'http_client'):
        app.state.http_client = httpx.AsyncClient()
    return app.state.http_client

def get_note_service(http_client: httpx.AsyncClient = Depends(get_http_client)):
    return NoteService(http_client=http_client, repository=note_repo)

async def get_summary_service(http_client: httpx.AsyncClient = Depends(get_http_client)) -> SummaryService:
    return SummaryService(http_client)

@router.get("", response_model=list[GetNotes])
async def get_all(database: AsyncSession = Depends(get_database_session)):
    return await note_repo.get_all_notes(database)

@router.post("", response_model=GetNotes, status_code=status.HTTP_201_CREATED)
async def create(
    note_data: CreateNotes, 
    database: AsyncSession = Depends(get_database_session), 
    summary_service:SummaryService = Depends(get_summary_service),
    notes_service:NoteService = Depends(get_note_service)
):
    return await notes_service.create_notes(database, note_data, summary_service)

@router.get("/{note_id}", response_model=GetNotes)
async def read( note_id: str, database: AsyncSession = Depends(get_database_session)):
    return await note_repo.get_notes(database, note_id)

@router.put("/{note_id}", response_model=GetNotes)
async def updare(
    note_id: str,
    note_data: UpdateNotes, 
    database: AsyncSession = Depends(get_database_session), 
    summary_service = Depends(get_summary_service),
    notes_service:NoteService = Depends(get_note_service)
    ):
   return await notes_service.update_note(database, note_id, note_data, summary_service)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    note_id: str, 
    database: AsyncSession = Depends(get_database_session),
    notes_service:NoteService = Depends(get_note_service)):
    await notes_service.delete_notes(database, note_id)
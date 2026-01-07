from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.note import Note
from app.core.exceptions import GlobalExceptionHandler
from app.schemas.note import UpdateNotes


async def create_notes(database:AsyncSession, note_data:Note):
    database.add(note_data)
    await database.commit()
    await database.refresh(note_data)
    return note_data

async def get_all_notes(database:AsyncSession):
    result = await database.execute(select(Note))
    return result.scalars().all()

async def get_notes(database:AsyncSession, id):
    result = await database.execute(select(Note).where(Note.id == id))
    note_data = result.scalar_one_or_none()
    if not note_data:
        raise GlobalExceptionHandler
    return note_data

async def delete_notes(database: AsyncSession, note_id: str) -> None:
    note = await get_notes(database, note_id)
    await database.execute(delete(Note).where(Note.id == note_id))
    await database.commit()

async def update_notes(session: AsyncSession, note_id: str, note_data: UpdateNotes, summary: str) -> Note:
    note = await get_notes(session, note_id)
    note.title = note_data.title
    note.content = note_data.content
    note.ai_summary = summary
    await session.commit()
    await session.refresh(note)
    return note
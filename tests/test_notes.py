@pytest.mark.asyncio
async def test_create(client, monkeypatch):
    async def fake_summary(self, content: str):
        return "mocked summary"

    from app.services.note_service import SummaryService
    monkeypatch.setattr(SummaryService, "generate_summary", fake_summary)

    response = await client.post("/notes", json={
        "title": "Test",
        "content": "This is a test note content"
    })

    assert response.status_code == 201
    assert response.json()["ai_summary"] == "mocked summary"

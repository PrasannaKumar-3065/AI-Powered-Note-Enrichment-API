import pytest

@pytest.mark.asyncio
async def test_create(client, monkeypatch):
    async def fake_generate_summary(self, text: str):
        return "mocked summary"

    # ✅ Mock the class method correctly
    monkeypatch.setattr(
        "app.services.note_service.SummaryService.generate_summary",
        fake_generate_summary
    )

    response = await client.post(
        "/notes",
        json={
            "title": "Test",
            "content": "This is a test note content"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["ai_summary"] == "mocked summary"

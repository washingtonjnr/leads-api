import pytest
from unittest.mock import AsyncMock, MagicMock, patch

class TestLeadRepository:
    async def test_create(self, lead_repository, valid_lead_create_schema):
        lead_repository.collection.insert_one = AsyncMock()

        with patch(
            "app.repositories.base.get_next_sequence",
            new_callable=AsyncMock,
            return_value=1
        ):
            with patch("uuid.uuid4", return_value="uuid-test"):
                result = await lead_repository.create(valid_lead_create_schema)

        assert result.name == "John Doe"
        assert result.email == "john@example.com"

        lead_repository.collection.insert_one.assert_called_once()

    async def test_find_by_id(self, lead_repository, mock_lead):
        lead_repository.collection.find_one = AsyncMock(return_value=mock_lead)

        result = await lead_repository.find_by_id("1")

        assert result.email == "john@example.com"

        lead_repository.collection.find_one.assert_called_once_with({"_id": 1})

    async def test_find_by_id_not_found(self, lead_repository):
        lead_repository.collection.find_one = AsyncMock(return_value=None)

        result = await lead_repository.find_by_id("1")

        assert result is None

    async def test_find_by_external_id(self, lead_repository, mock_lead):
        lead_repository.collection.find_one = AsyncMock(return_value=mock_lead)

        result = await lead_repository.find_by_external_id("uuid-123")

        assert result.email == "john@example.com"

        lead_repository.collection.find_one.assert_called_once_with(
            {"external_id": "uuid-123"}
        )

    async def test_find_by_external_id_not_found(self, lead_repository):
        lead_repository.collection.find_one = AsyncMock(return_value=None)

        result = await lead_repository.find_by_external_id("uuid-123")

        assert result is None

    async def test_get_by_email(self, lead_repository, mock_lead):
        lead_repository.collection.find_one = AsyncMock(return_value=mock_lead)

        result = await lead_repository.get_by_email("john@example.com")

        assert result.email == "john@example.com"

        lead_repository.collection.find_one.assert_called_once_with(
            {"email": "john@example.com"}
        )

    async def test_get_by_email_not_found(self, lead_repository):
        lead_repository.collection.find_one = AsyncMock(return_value=None)

        result = await lead_repository.get_by_email("john@example.com")

        assert result is None

    async def test_find_all(self, lead_repository, mock_lead):
        cursor = MagicMock()
        cursor.__aiter__.return_value = [mock_lead]

        lead_repository.collection.find = MagicMock(return_value=cursor)

        result = await lead_repository.find_all()

        assert len(result) == 1
        assert result[0].email == "john@example.com"

    async def test_find_paginated(self, lead_repository, mock_lead):
        lead_repository.collection.count_documents = AsyncMock(return_value=1)

        cursor = MagicMock()
        cursor.skip.return_value = cursor
        cursor.limit.return_value = cursor
        cursor.__aiter__.return_value = [mock_lead]

        lead_repository.collection.find = MagicMock(return_value=cursor)

        result, total = await lead_repository.find_paginated(1, 10)

        assert total == 1
        assert len(result) == 1

    async def test_update(self, lead_repository, mock_lead):
        lead_repository.collection.update_one = AsyncMock()

        lead_repository.find_by_id = AsyncMock(return_value=MagicMock(**mock_lead))

        result = await lead_repository.update("1", {"name": "Updated"})

        lead_repository.collection.update_one.assert_called_once_with(
            {"_id": 1},
            {"$set": {"name": "Updated"}},
        )

        assert result is not None

    async def test_delete(self, lead_repository):
        delete_result = MagicMock()
        delete_result.deleted_count = 1

        lead_repository.collection.delete_one = AsyncMock(return_value=delete_result)

        result = await lead_repository.delete("1")

        lead_repository.collection.delete_one.assert_called_once_with({"_id": 1})

        assert result is True
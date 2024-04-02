import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, AsyncMock
from pizza_api.repository.interface.order_repo import IOrderRepo
from pizza_api.usecases.order_usecase.get_specific_order_usecase import GetSpecificOrderUsecase


class TestSpecificOrder:

    @pytest.mark.asyncio
    async def test_orchestrate(self, mocker: MockerFixture):
        self._mocker = mocker
        await self.perform_specific_order()
        await self.perform_specific_order_does_not_exist()

    def mock_repo(self):
        return Mock(spec=IOrderRepo)
    
    async def perform_specific_order(self):
        repo = self.mock_repo()
        json_data = {
            "pizza_size": {
                "code": "LARGE",
                "value": "large"
            },
            "id": 2,
            "quantity": 2,
            "order_status": {
                "code": "PENDING",
                "value": "pending"
            },
            "user_id": 2
        }

        self._mocker.patch.object(
            target=repo,
            attribute="get_specific_order",
            side_effect=AsyncMock(return_value=json_data)
        )

        usecase = GetSpecificOrderUsecase(repo)
        res = await usecase.execute(order_id=2)

        assert res is not None
        assert isinstance(res, dict)
        assert res["id"] == 2

    async def perform_specific_order_does_not_exist(self):
        repo = self.mock_repo()
        json_data = {
                            "detail": "No order with such id"
                    }

        self._mocker.patch.object(
            target=repo,
            attribute="get_specific_order",
            side_effect=AsyncMock(return_value=json_data)
        )

        usecase = GetSpecificOrderUsecase(repo)
        res = await usecase.execute(order_id=2)

        assert res is not None
        assert isinstance(res, dict)
        assert res == json_data

        
    
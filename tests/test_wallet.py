import pytest


@pytest.mark.asyncio
async def test_deposit_and_get(client):
	# Делаем депозит
	resp = await client.post(
		"/v1/1/operation",
		json={"operation_type": "DEPOSIT", "amount": 10},
	)
	assert resp.status_code == 200
	data = resp.json()
	assert data["status"] == "success"
	assert float(data["amount"]) == 10.0

	# Получаем кошелёк
	resp2 = await client.get("/v1/wallets/1")
	assert resp2.status_code == 200
	data2 = resp2.json()
	assert float(data2["amount"]) == 10.0


@pytest.mark.asyncio
async def test_withdraw_flow(client):
	# Подготовка: депозит 20
	resp1 = await client.post(
		"/v1/2/operation",
		json={"operation_type": "DEPOSIT", "amount": 20},
	)
	assert resp1.status_code == 200

	# Успешный вывод 5
	resp2 = await client.post(
		"/v1/2/operation",
		json={"operation_type": "WITHDRAW", "amount": 5},
	)
	assert resp2.status_code == 200
	assert float(resp2.json()["amount"]) == 15.0

	# Недостаточно средств
	resp3 = await client.post(
		"/v1/2/operation",
		json={"operation_type": "WITHDRAW", "amount": 100},
	)
	assert resp3.status_code == 400
	assert resp3.json()["detail"] == "Insufficient balance"



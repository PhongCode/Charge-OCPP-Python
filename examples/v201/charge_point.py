import asyncio

from ocpp.v201.enums import RegistrationStatusType, AuthorizationStatusType, RequestStartStopStatusType
import logging
import websockets

from ocpp.v201 import call
from ocpp.v201 import ChargePoint as cp

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={
                'model': 'Wallbox XYZ',
                'vendor_name': 'anewone'
            },
            reason="PowerUp"
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            print("Connected to central system.")

    async def authorize(self):
        request = call.AuthorizePayload(
            id_token={
                'id_token': 'AA12345',
                'type': 'ISO14443'
            }
        )
        response = await self.call(request)
        if response.id_token_info['status'] == AuthorizationStatusType.accepted:
            print("Authorization successfully.")

    async def start_transaction(self):
        request = call.RequestStartTransactionPayload(
            id_token={
                'id_token': 'AA12345',
                'type': 'ISO14443'
            },
            remote_start_id=1
        )
        response = await self.call(request)
        if response.status == RequestStartStopStatusType.accepted:
            print('You can start transaction.')


async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_1',
            subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.authorize(), cp.start_transaction())


if __name__ == '__main__':
    asyncio.run(main())
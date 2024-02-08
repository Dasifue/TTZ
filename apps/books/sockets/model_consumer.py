import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.db.models.query import QuerySet


class ModelConsumer(AsyncWebsocketConsumer):
    serializer_class = None
    model = None
    queryset: QuerySet[model] = None
    prefetch_related = None
    action_preffix: str = "object"

    async def connect(self):
        self.room_group_name = "books"

        await self.accept()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.send(json.dumps({
            "type": "connection_established",
            "message": "You are now connected!"
        }))

        asyncio.create_task(self.send_objects())

    
    async def receive(self, text_data: str):
        try:
            data = json.loads(text_data)
        except json.decoder.JSONDecodeError as error:
            await self.send(json.dumps({
                "type": "answer",
                "errors": str(error),
            }))
        else:
            type_ = data.get("type")

            if type_ == f"{self.action_preffix}.create":
                await self.create(data)
            elif type_ == f"{self.action_preffix}.update":
                await self.update(data)
            elif type_ == f"{self.action_preffix}.partial_update":
                await self.partial_update(data)
            elif type_ == f"{self.action_preffix}.delete":
                await self.delete(data)
            elif type_ == f"{self.action_preffix}.get":
                await self.get(data)
            else:
                await self.send(json.dumps({
                    "type": "answer",
                    "errors": "Неправильный тип запроса"
                }, ensure_ascii=False))

        

    async def create(self, data: dict, notification: bool = False):
        serializer = self.serializer_class(data=data.get("data"))
        if serializer.is_valid():
            await sync_to_async(serializer.save)()

            await self.send(json.dumps({
                "type": "answer",
                "data": json.dumps(serializer.data, ensure_ascii=False)
            }, ensure_ascii=False))

            if notification:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "notification",
                        "message": f"Новый(ая) {serializer.Meta.model}!"
                    }
                )
        else:
            await self.send(json.dumps({
                "type": "answer",
                "errors": json.dumps(serializer.errors, ensure_ascii=False)
            }, ensure_ascii=False))


    async def pre_update(self, data:dict, **kwargs):
        pk = data.get(f"{self.action_preffix}.id")

        if not pk:
            await self.send(json.dumps({
                "type": "answer",
                "errors": f"{self.action_preffix}.id не был предоставлен!"
            }, ensure_ascii=False))

        try:
            instance = await sync_to_async(self.model.objects.get)(
                pk=pk
            )
        except self.model.DoesNotExist:
            await self.send(json.dumps({
                "type": "answer",
                "errors": f"{self.action_preffix}.id неверный!"
            }, ensure_ascii=False))
        else:
            serializer = self.serializer_class(instance=instance, data=data.get("data"), **kwargs)
            if serializer.is_valid():
                await sync_to_async(serializer.save)()
                await self.send(json.dumps({
                    "type": "answer",
                    "data": json.dumps(serializer.data, ensure_ascii=False)
                }, ensure_ascii=False))
            else:
                await self.send(json.dumps({
                    "type": "answer",
                    "data": json.dumps(serializer.errors, ensure_ascii=False)
                }, ensure_ascii=False))


    async def update(self, data: dict):
        await self.pre_update(data=data)
        

    async def partial_update(self, data: dict):
        await self.pre_update(data=data, partial=True)

    async def delete(self, data: dict):
        pk = data.get(f"{self.action_preffix}.id")
        if not pk:
            await self.send(json.dumps({
                "type": "answer",
                "errors": f"{self.action_preffix}.id не был предоставлен!"
            }, ensure_ascii=False))
        else:
            coroutine = await sync_to_async(self.model.objects.filter)(pk=pk)
            await sync_to_async(coroutine.delete)()
            await self.send(json.dumps({
               "type": "answer",
               "message": "Удалено!" 
            }, ensure_ascii=False))


    async def get(self, data: dict):
        pk = data.get(f"{self.action_preffix}.id")
        if not pk:
            await self.send(json.dumps({
                "type": "answer",
                "errors": f"{self.action_preffix}.id не был предоставлен!"
            }, ensure_ascii=False))
        else:
            try:
                instance = await sync_to_async(self.model.objects.get)(pk=pk)
            except self.model.DoesNotExist:
                await self.send(json.dumps({
                "type": "answer",
                "error": "Не найден!" 
                }, ensure_ascii=False))
            else:
                serializer = self.serializer_class(instance=instance)
                await self.send(json.dumps({
                "type": "answer",
                "data": json.dumps(serializer.data, ensure_ascii=True)
                }, ensure_ascii=False))


    async def notification(self, event: dict):
        message = event['message']
        await self.send(json.dumps({"message": message}, ensure_ascii=False))

    
    async def send_objects(self):
        while True:
            if self.prefetch_related:  
                instances = await sync_to_async(
                lambda: list(
                    self.queryset.prefetch_related(self.prefetch_related)
                )
                )()  
            else:
                instances = await sync_to_async(list)(self.queryset) 
            serializer = self.serializer_class(instance=instances, many=True)
            serialized_data = serializer.data
            await self.send(json.dumps({
                "type": "data",
                "data": serialized_data
            }, ensure_ascii=False))
            await asyncio.sleep(60)


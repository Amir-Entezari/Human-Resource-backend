from ninja import NinjaAPI
from human_resource_app.apis import router as human_resource_app_router


api = NinjaAPI()

api.add_router("/human-resource/", human_resource_app_router)
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from schemas.s3_schema import PresignedPostRequest
from security.user_session import UserSession, authorize, get_current_user
from services.provider.s3_service import s3_service

router = InferringRouter(tags=["S3"])


@cbv(router)
class S3Router:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/s3/presigned-request")
    def get_presigned_post(self, payload: PresignedPostRequest):
        presigned_post = s3_service.generate_presigned_post(
            file_extension=payload.file_extension, content_type=payload.content_type
        )
        return presigned_post

from schemas.base_schema import BaseSchema


class PresignedPostRequest(BaseSchema):
    content_type: str
    file_extension: str

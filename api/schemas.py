from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title:str
    description:str

class OutputArticleSchema(ArticleSchema):
    id:int
    class Config:
        orm_mode=True

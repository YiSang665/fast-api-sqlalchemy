from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models
from .schemas import ArticleSchema, OutputArticleSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def index():
    return {"message": "Hello World !!!"}


@app.post('/articles', status_code=status.HTTP_201_CREATED)
def add_article(article:ArticleSchema, db: Session=Depends(get_db)):
    new_article = models.Article(title=article.title,
                                 description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.get('/articles', response_model=List[OutputArticleSchema])
def get_articles(db: Session=Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles

@app.get('/articles/{id}', response_model=OutputArticleSchema,
         status_code=status.HTTP_200_OK)
def article_details(id:int, db: Session=Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id==id).first()
    if article:
        return article
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found.")

@app.put('/articles/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id:int, article:ArticleSchema, db: Session=Depends(get_db)):
    db.query(models.Article).filter(models.Article.id==id).update({
        "title": article.title, "description": article.description
    })
    db.commit()
    return {'message': 'The data is updated.'}

@app.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id:int, db: Session=Depends(get_db)):
    db.query(models.Article).filter(models.Article.id==id).delete(
        synchronize_session=False)
    db.commit()
    

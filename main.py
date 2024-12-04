from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import session
import models
import schema
from database import engine,get_db

app =  FastAPI()

models.Base.metadata.create_all(bind = engine)

#3. Create end points that will be able to make a post, update a post and delete a post as well as get a single post by id.

#get all the posts
@app.get("/get_posts/")
async def get_post(db: session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#get post by id 
@app.get('/get_post/{id}')
async def get_post(id:int, db: session = Depends(get_db)):
    #fetch the post from the database 
    post = db.query(models.Post).filter(models.Post.id == id ).first()

    #return the post
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="post not found")


#create a post
@app.post('/create_posts/')
async def create_post(post:schema.Post, db: session = Depends(get_db)):
    new_post_dic = post.model_dump()
    new_post = models.Post(**new_post_dic)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return [new_post]


#update a post
@app.put('/update_post/{id}')
async def update_post(id:int, post : schema.Post, db: session = Depends(get_db)):
    post_update_dic = post.model_dump()

    #fetch the post from the database 
    post_to_update = db.query(models.Post).filter(models.Post.id == id )
    
    if post_to_update:
        #update the post the fetched post with the request body info
        post_to_update.update(post_update_dic)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail= "Post not found")
    
#delete a post
@app.delete('/delete_post/{id}')
async def delete_post(id:int, db : session=Depends(get_db)):
    #fetch the post from the database 
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()

    #delete from the database
    if post_to_delete:
        db.delete(post_to_delete)
        db.commit()
        raise HTTPException(status_code=200, detail="the post has been deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="post was not found")



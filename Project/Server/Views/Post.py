from bson import ObjectId
from fastapi import APIRouter, Body
from Server.Database import Post_collection
from Server.Utils.Image_Handler import Image_Converter
from Server.Controller.Post import Add_Post,Delete_Old_Image,Check_Post, retrieve_all_Post, retrieve_Post_by_id, delete_Post_data, update_Post
from Server.Models.Post import Posts
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_description="Add Post")
async def add_Posts_data(schema: Posts = Body(...)):
    schema = jsonable_encoder(schema)
    Post= await Check_Post(schema)
    if Post== False:
        return {"code": 200, "Msg":"Post already exists"}
    if len(schema['IMAGE'])>0:    
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Post(schema)
    return {"code": 200, "Msg": Output}


@router.get("/", response_description="Get all Posts")
async def get_all_Posts():
    Posts = await retrieve_all_Post()
    if Posts:
        return {"code": 200, "Data": Posts}
    return {"Data": Posts, "Msg": "Empty list return"}


@router.get("/{id}", response_description="Get Post data by id")
async def get_Post_data(id):
    data = await retrieve_Post_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/{id}", response_description="Delete Post data by id")
async def delete_Post(id: str):
    data = await delete_Post_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/{id}")
async def update_Post_data(id: str, req: Posts = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    flags=0
    if len(req["IMAGE"])!=0:
        Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_Post = await update_Post(id, req,flags)
    if updated_Post:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }


@router.post("/{id}", response_description="Change Post Status")
async def Change_Post_Status(id: str):
    data = await Post_collection.find_one({"_id":ObjectId(id)})
    if data:
        if data["Status"]=="Active":
            await Post_collection.update_one({"_id":ObjectId(id)},{"$set":{"Status":"Inactive"}})
        else:
            await Post_collection.update_one({"_id":ObjectId(id)},{"$set":{"Status":"Active"}})
        return {"code": 200, "Data": "Status Changed Successfully"}
    return {"code": 404, "Data": "Id may not exist"}
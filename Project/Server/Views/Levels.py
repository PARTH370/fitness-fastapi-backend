import base64
import uuid
from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Levels import Add_Level,Delete_Old_Image,Check_Level, delete_Level_data, retrieve_all_Levels, retrieve_Level_by_id, update_Level
from Project.Server.Models.Levels import Levels
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/Add_Levels", response_description="Add Level")
async def add_Levels_data(schema: Levels = Body(...)):
    schema = jsonable_encoder(schema)
    Level =await Check_Level(schema)
    if Level==False:
        return {"code": 200, "Msg":"Levels already exists"}
    if len(schema['IMAGE'])>0:    
        img_path= await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Level(schema)
    return {"code": 200, "Msg": Output}


@router.get("/Get_all_Levels", response_description="Get all Levels")
async def get_all_Levels():
    Levels = await retrieve_all_Levels()
    if Levels:
        return {"code": 200, "Data": Levels}
    return {"Data": Levels, "Msg": "Empty list return"}


@router.get("/Get_Level_Data/{id}", response_description="Get Level data by id")
async def get_Level_data(id):
    data = await retrieve_Level_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete Level data by id")
async def delete_Level(id: str):
    data = await delete_Level_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_Level_data(id: str, req: Levels = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    flags=0
    if len(req["IMAGE"])!=0:
        # Del_img= await Delete_Old_Image(id)
        Image_Path=await Image_Converter(req["IMAGE"])
        req["IMAGE"]=Image_Path
        flags=1
    updated_Level = await update_Level(id, req,flags)
    if updated_Level:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }

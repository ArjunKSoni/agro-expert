from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

import soil
import search_crop as sc
import crop_json as cj
import crop
model_soi,ind,df1=soil.model()
model_cr,inde2=crop.model()
model_soil=model_soi
index=ind
df=df1
model_crop=model_cr
index2=inde2


class Item1(BaseModel):
    search: str

class Item2(BaseModel):
    N: int
    P:int
    K:int
    temperature:int
    humidity:int
    rainfall:int
    ph:int
    label:str

class Item3(BaseModel):
    N: int
    P:int
    K:int
    temperature:int
    humidity:int
    rainfall:int
    ph:int



app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def first():
    return("successfully loaded")

@app.post("/nav")
async def create_item(item: Item1):
    crop=item.search
    p=sc.search(crop)
    if p==-1:
        json_compatible_item_data = jsonable_encoder({"status":"fail"})
        return JSONResponse(content=json_compatible_item_data)
    k=df[df['label']==p[0]]['Sno'].values[0]
    crop_detail=[]
    crop_img=[]
    crop_name=[]
    pi=[]
    for i in range(4):
        crop_detail.append(cj.find(p[i]))
        crop_img.append(crop_detail[i]["img"])
        crop_name.append(crop_detail[i]["name"].upper())
    crop_desc=crop_detail[0]["desc"]
    pi=df[df['Sno']==k].values[0].tolist()
    re={"crop":pi, "ci":crop_img, "cn":crop_name, "cd":crop_desc,"status":"success"}
    json_compatible_item_data = jsonable_encoder(re)
    return JSONResponse(content=json_compatible_item_data)



@app.post("/get_soil_info")
async def create_item(item: Item2):
    N=item.N
    P=item.P
    K=item.K
    temperature=item.temperature
    humidity=item.humidity
    ph=item.ph
    rainfall=item.rainfall
    label=item.label
    val=[N,P,K,temperature,humidity,ph,rainfall]
    p=sc.search(label)
    if p==-1:
        json_compatible_item_data = jsonable_encoder({"status":"fail"})
        return JSONResponse(content=json_compatible_item_data)  
    global inde
    for i in index:
        if(i[0]==p[0]):
            val.append(i[1])
            break
    predicted=soil.predict(val,model_soil,index)
        
    crop_detail=[]
    crop_img=[]
    crop_name=[]
    for i in range(4):
        crop_detail.append(cj.find(p[i]))
        crop_img.append(crop_detail[i]["img"])
        crop_name.append(crop_detail[i]["name"].upper())
    crop_desc=crop_detail[0]["desc"]
    re={ "crop":predicted,"ci":crop_img, "cn":crop_name, "cd":crop_desc,"status":"success"}
    json_compatible_item_data = jsonable_encoder(re)
    return JSONResponse(content=json_compatible_item_data)

@app.post("/get_crop_info")
async def create_item(item: Item3):
    N=item.N
    P=item.P
    K=item.K
    temperature=item.temperature
    humidity=item.humidity
    ph=item.ph
    rainfall=item.rainfall
    val=[N,P,K,temperature,humidity,ph,rainfall]
    predicted=crop.predict(val,model_crop,index2)
    p=sc.search(predicted[8])
    if p==-1:
        json_compatible_item_data = jsonable_encoder({"status":"fail"})
        return JSONResponse(content=json_compatible_item_data) 
    crop_detail=[]
    crop_img=[]
    crop_name=[]
    for i in range(4):
        crop_detail.append(cj.find(p[i]))
        crop_img.append(crop_detail[i]["img"])
        crop_name.append(crop_detail[i]["name"].upper())
    crop_desc=crop_detail[0]["desc"]

    re={"crop":predicted, "ci":crop_img, "cn":crop_name, "cd":crop_desc,"status":"success"}
    json_compatible_item_data = jsonable_encoder(re)
    return JSONResponse(content=json_compatible_item_data)

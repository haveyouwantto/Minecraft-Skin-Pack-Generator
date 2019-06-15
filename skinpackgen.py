# -*- coding: utf-8 -*-
import uuid
import json
import random
import os
from pathlib import Path
from shutil import copyfile
import fnmatch

skinfolder=input("皮肤输入文件夹：")#r"C:\Users\havey\Desktop\mcskins\skins"
outfolder=Path(input('Minecraft皮肤包文件夹：'))#r"C:\Users\havey\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\skin_packs\bigpack")
name=input('皮肤包名称（仅限英文）：')

lid=hex(random.randint(0,65535))

if (outfolder.exists()==False):
    print("创建 "+str(outfolder))
    os.mkdir(outfolder)

def manifest(out,name):
    uuid1=uuid.uuid4()
    uuid2=uuid.uuid4()
    outcontent=json.dumps({
    "format_version": 1,
    "header": {
        "name": name,
        "uuid": str(uuid1),
        "version": [
            1,
            0,
            0
        ]
    },
    "modules": [
        {
            "type": "skin_pack",
            "uuid": str(uuid2),
            "version": [
                1,
                0,
                0
            ]
        }
    ]
    }
                          )
    manifest=open((str(outfolder)+"/manifest.json"),"w")
    print("创建 "+str(manifest))
    manifest.write(outcontent)
    manifest.close()

def skinconv(skinfolder,outfolder,name,lid):
    
    #skinout=Path(str(outfolder)+"/skins")
    texts=Path(str(outfolder)+"/texts")

    #if (skinout.exists()==False):
     #   print("创建 "+str(skinout))
     #   os.mkdir(skinout)
    if (texts.exists()==False):
        print("创建 "+str(texts))
        os.mkdir(texts)
    
    skins='''{
  "geometry": "skinpacks/skins.json",
  "skins": [
          '''
    langs=open((str(texts)+"/languages.json"),"w")
    print("创建 "+str(langs))
    langs.write('''
    [
      "en_US"
    ]''')
    langs.close()

    langtext=open((str(texts)+"/en_US.lang"),"w")
    print("创建 "+str(langtext))
    langtext.write(u'skinpack.'+lid+'='+name+"\n\n")

    filelist=os.listdir(skinfolder)
    for filename in filelist:
        filepath=os.path.join(skinfolder,filename)
        fnclean=filename[:-4]
        if fnmatch.fnmatch(filepath,'*.png'):
            print("添加 "+filename)
            copyfile(filepath,str(outfolder)+"/"+filename)
            skins+=u'''
            {
          "localization_name": "'''+fnclean+'''",
          "geometry": "geometry.humanoid.custom",
          "texture": "'''+filename+'''",
          "type": "free"
            },'''
            langtext.write(u'skin.'+lid+"."+fnclean+"="+fnclean+"\n")
            
    skins=skins[:-1]
    skins+=u'''
    ],
      "serialize_name": "'''+name+'''",
      "localization_name": "'''+lid+'''"
    }
            '''
    skinf=open((str(outfolder)+"/skins.json"),"w")
    print("创建 "+str(skinf))
    skinf.write(skins)
    skinf.close()

            
manifest(outfolder,name)
skinconv(skinfolder,outfolder,name,lid)

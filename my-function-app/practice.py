import logging
from os import environ
from typing import List, Optional,Tuple
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json


collectionName = input("collectionName\n")
applicationName = input("application\n")
processDate = input("processDate\n")




def parse_blob_path(path: Optional[str]) -> Tuple[str,str,str,str,str,str]:
    if not path:
        raise ValueError("Expected string, received None")
    parts=path.split("/")
    print(parts)
    
    if parts[1] == "dbfs":
        parts=parts[3:]
        
    zone=parts[1]
    source=parts[2]
    usecase=parts[3].split("=")[1]
    date=parts[4].split("=")[1]
    filename=parts[5]
    print(filename)
    return (zone+"/"+source+"/"+usecase+"/"+date+"/"+filename)

#k=parse_blob_path(f"/dbfs/mnt/acquisitionlayer/landingzone/purview/application={applicationName}/date={processDate}/")
k=parse_blob_path(f"acquisitionlayer/landingzone/purview/application={applicationName}/date={processDate}/")
print(k)







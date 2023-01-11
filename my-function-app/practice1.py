import logging
import os
from os import environ
from typing import List, Optional,Tuple
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import json


def func(collectionName,applicationName,processDate):
    
    def parse_blob_path(path: Optional[str]) -> Tuple[str,str,str,str,str,str]:
        if not path:
            raise ValueError("Expected string, received None")
        parts=path.split("/")
        print(parts)
        zone=parts[4]
        source=parts[5]
        usecase=parts[6].split("=")[1]
        date=parts[7].split("=")[1]        
        filename=parts[8]
        return (zone+"/"+source+"/"+usecase+"/"+date+"/"+filename)
    path=parse_blob_path(f"/dbfs/mnt/acquisitionlayer/landingzone/purview/application={applicationName}/date={processDate}/")
      
    return collectionName,applicationName,processDate,path


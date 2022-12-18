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

def func(collectionName,applicationName,processDate):
    
    def parse_blob_path(path: Optional[str]) -> Tuple[str,str,str,str,str,str]:
        if not path:
            raise ValueError("Expected string, received None")
        parts=path.split("/")
        zone=parts[4]
        source=parts[5]
        usecase=parts[6].split("=")[1]
        date=parts[7].split("=")[1]        
        filename=parts[8]
        return (zone+"/"+source+"/"+usecase+"/"+date+"/"+filename)
    k=parse_blob_path(f"/dbfs/mnt/acquisitionlayer/landingzone/purview/application={applicationName}/date={processDate}/")
    print(k)  
    return collectionName,applicationName,processDate



auth=ServicePrincipalAuthentication(
    tenant_id=f"{tenant_id}",
    client_id=purview_client_id,
    client_secret=purview_client_secret    
)

client=PurviewClient(
    account_name=purview_account_name,
    authentication=auth)
    
def get_secrets(req_secrets: List[str]) -> None:
    kv_name=environ["KEY_VAULT_NAME"]
    kv_url=f"https://{kv_name}.vault.azure.net"
    client_id=environ["azureClientId"]
    logging.info("Loading secrets from KV to environment")
    credential=ManagedIdentityCredential(client_id=client_id)
    client=SecretClient(vault_url=kv_url,credential=credential)
    secretlist=client.list_properties_of_secrets()
    for secret in secretlist:
        if secret.name in req_secrets:
            environ[secret.name]=client.get_secret(secret.name).value







entityList=[]
relationshipList=[]
entitiesDict={}
relationshipsDict={}
allTypeDefs=client.get_all_typedefs()
entityTypedefs = allTypeDefs["entityDefs"]
collectionAPIData=client.collections.list_collections()
print(collectionAPIData)

for collection in collectionAPIData:
    if collection["friendlyName"]==f"{collectionName}":
        collectionId =collection["name"]
        collectionName=collection["name"]

        for entityTypeDef in entityTypedefs:
            if entityTypeDef["name"] in (
                "azure_datalake_gen2_path",
                "azure_datalake_gen2_resource_set",
                "azure_datalake_gen2_filesystem",
                "azure_datalake_gen2_object",
                "azure-datalake_gen2_service",
            ):
                queryFilter={
                    "and": [
                        {"entityType":entityTypeDef["name"]},
                        {"collectionId":collectionId}
                    ]
                }
                queryAPIData=client.discovery.query(filter=queryFilter)

                if queryAPIData["@search.count"] > 0:
                    for entity in queryAPIData["value"]:
                        entityDict={}
                        entityDetails = client.get_single_entity(guid=entity["id"])

                        if entityTypeDef["name"] == "azure_datalake_gen2_seervice":
                            entityDict["entityObjectType"] = "Interface"
                        else:
                            entityDict["entityObjectType"] = entity["objectType"]
                        
                        entityDict["entityDetails"]=entityDetails["entity"]
                        entityList.append(entityDict)

                        for key,value in entityDetails["entity"]["relationshipAttributes"].items():
                            if key == "attachedSchema":
                                for schemaDetails in entityDetails["entity"]["relationshipAttributes"]["attachedSchema"]:
                                    schemaEntityDetails =client.get_single_entity(guid=schemaDetails["guid"])

                                    if schemaEntityDetails["referredEntities"]:

                                        for (refEntityId,refEntityDetails) in schemaEntityDetails["referredEntities"].items():
                                            entityDict={}
                                            entityDict["entityObjectType"]=refEntityDetails["typename"]
                                            entityDict["entityDetails"] = refEntityDetails

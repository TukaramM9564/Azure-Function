import os, uuid
from pathlib import Path
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

    accountName = "azureblobfunc"
    accountKey = "/eYcq1SIZPb/jF8dUt5SyTDeZ+4MP3u2QlvIUKljmm6DsglBqIfsr9QEoCgGh5szZYH0mltzwpBb+AStVa69HA=="
    account_URL="https://azureblobfunc.blob.core.windows.net/"
 
    connect_str="DefaultEndpointsProtocol=https;AccountName=azureblobfunc;AccountKey=x0EZtOoIupaD1palCKSIPy4T9NglPhofyOkRxmEkvpX6RHQPQyXsxT1QGyQjWiVCWfBX5cfaifg/+AStj3v03A==;EndpointSuffix=core.windows.net"

    blobService = BlobServiceClient(account_name=accountName, account_key=accountKey, account_url= account_URL)
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "mycontainer"
    print("hello")

    # Create the container
    container_client = blob_service_client.create_container(container_name)

    print('current path--->', Path.cwd())
    # Upload the created file
   
    LOCAL_IMAGE_PATH=("C:\\Users\\TSATYAWA\\OneDrive - Capgemini\\Desktop\\Tukaram")
    
    class AzureBlobFileUploader:
        def __init__(self):
            print("Intializing AzureBlobFileUploader")
 
    # Initialize the connection to Azure storage account
            self.blob_service_client =  BlobServiceClient.from_connection_string(connect_str)
 
        def upload_all_images_in_folder(self):
    # Get all files with jpg extension and exclude directories
            all_file_names = [f for f in os.listdir(LOCAL_IMAGE_PATH)
                    if os.path.isfile(os.path.join(LOCAL_IMAGE_PATH, f)) and ".txt" in f]
 
    # Upload each file
            for file_name in all_file_names:
                print("uploading..."+file_name)
                self.upload_image(file_name)
 
        def upload_image(self,file_name):
    # Create blob with same name as local file name
            blob_client = self.blob_service_client.get_blob_client(container=container_name,
                                                          blob=file_name)
    # Get full path to the file
            upload_file_path = os.path.join(LOCAL_IMAGE_PATH, file_name)
            blob_client.upload_blob(upload_file_path)
            print("uploaded")
             
# Initialize class and upload files
    azure_blob_file_uploader = AzureBlobFileUploader()
    azure_blob_file_uploader.upload_all_images_in_folder()
except Exception as ex:
    print('Exception:')
    print(ex)
from google.cloud import storage
bucketName="desarrollocloud2018461201105"

def upload_to_bucket(fileName, path_to_file):
    storage_client = storage.Client.from_service_account_json(
        'creds.json')
    bucket = storage_client.get_bucket(bucketName)
    blob = bucket.blob(fileName)
    blob.upload_from_filename(path_to_file)
    return blob.public_url


def  downloadFile(fileName):
    path_to_private_key = ' creds.json'
    client = storage.Client.from_service_account_json( json_credentials_path=path_to_private_key)
    bucket = storage.Bucket(client, bucketName)
    blob = bucket.blob(fileName)
    blob.download_to_filename(fileName)
    

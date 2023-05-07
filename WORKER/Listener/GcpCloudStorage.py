from google.cloud import storage


bucketName="desarrollocloud2018461201105"

def upload_to_bucket(fileName, path_to_file,folder):

    print("-------------------upload_to_bucket---------------------")
    storage_client = storage.Client.from_service_account_json(
        'creds.json')

    print(bucketName)
    print(fileName)
    print(path_to_file)
    print(folder)

    bucket = storage_client.get_bucket(bucketName)
    blob = bucket.blob(folder+fileName)
    try:
        
        blob.upload_from_filename(path_to_file)
    except Exception as e:
            print("Se presentó el siguiente error", e)
    
    print("upload_to_bucket")
    print( blob.public_url)
    return blob.public_url


def  downloadFile(fileName):
    path_to_private_key = ' creds.json'
    client = storage.Client.from_service_account_json( json_credentials_path=path_to_private_key)
    bucket = storage.Bucket(client, bucketName)
    blob = bucket.blob(fileName)
    blob.download_to_filename(fileName)
    

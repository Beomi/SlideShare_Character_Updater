import os
import boto3
import subprocess
import re
import urllib.parse
import time
# urllib.parse.unquote_plus

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER', 'downloads')

def download_from_s3(strBucket, s3_path, local_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3_client.download_file(strBucket, s3_path, local_path)

def upload_to_s3(bucket, s3_path, local_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3_client.upload_file(local_path, bucket, s3_path)
    
def make_public_read(bucket, key):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3_client.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)

def handler(event=None, context=None):
    bucket_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['bucket']['name'])
    file_path = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    # file_name = file_path.split('/')[-1]
    # bucket_name = event['bucket_name']
    # file_path = event['file_path']
    file_name = file_path.split('/')[-1]
    
    print('bucket_name: ', bucket_name)
    print('file_path: ', file_path)
    print('file_name: ', file_name)

    local_path = '/tmp/' + file_name
    print('local_path: ', local_path)

    download_from_s3(bucket_name, file_path, local_path)

    upload_s3_path = enable_korean(local_path, file_path)

    upload_to_s3(
        bucket_name, 
        upload_s3_path, 
        local_path
    )
        
    make_public_read(bucket_name, upload_s3_path)

    print('uploadPath: ', file_path.replace(UPLOAD_FOLDER, DOWNLOAD_FOLDER))
    
    return True

def get_langset(local_path):
    cmd = "cat {} | grep -a Ordering".format(local_path)
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    res = output.decode('utf-8')

    print('Result: ')
    print(res)

    lang_list = re.findall(r'Ordering ?\((\w+)\)', res)
    lang_set = set(lang_list)

    print('lang_set: ')
    print(lang_set)
    return lang_set

def convert_to_ko(lang, local_path):
    cmd = """
    LANG=C LC_ALL=C sed -ie 's:/Registry (Adobe) /Ordering ({}) /Supplement [0-9]:/Registry(Adobe) /Ordering(Identity) /Supplement 0:g' {}
    """.format(lang, local_path)
    print("CMD: ", cmd)
    ps = subprocess.Popen(cmd,shell=True, stderr=subprocess.STDOUT)

def enable_korean(local_path, file_path):
    lang_set = get_langset(local_path)

    for lang in lang_set:
        convert_to_ko(lang, local_path)
        time.sleep(2)
    
    if not 'Identity' in get_langset(local_path):
        print('Failed one time, try with 5s...')
        for lang in lang_set:
            convert_to_ko(lang, local_path)
            time.sleep(5)
    else:
        print("Success in one try! Good!")

    upload_s3_path = file_path.replace(UPLOAD_FOLDER, DOWNLOAD_FOLDER)

    return upload_s3_path


if __name__=='__main__':
    print(enable_korean('/downloads/test3.pdf', ''))

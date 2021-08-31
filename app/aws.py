from io import BytesIO
from base64 import b64decode
import os
import re

import boto3
import requests

FILE_URL = 'https://{bucket}.s3.us-east-2.amazonaws.com/{filename}'
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_GATEWAY_URL = os.getenv("AWS_GATEWAY_URL")


def _upload_to_s3(filename, content, bucket=AWS_S3_BUCKET):
    """Upload a file object to S3 returning its public URL

    Super helpfuL: https://stackoverflow.com/a/60239208
    """
    filename = re.sub(r"[^-_0-9a-z.]", r"", filename)
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket = s3_resource.Bucket(bucket)

    bucket.Object(filename).put(Body=content,
                                ACL='public-read')

    return FILE_URL.format(bucket=bucket.name,
                           filename=filename)


def create_audio_mix(
    req_phrase_filename,
    req_phrase_file_content_encoded,
    req_sound_filename,
    req_sound_file_content_encoded,
    **kwargs
):
    """Upload files to S3 and invoke apg in AWS Lambda

    TODO: have the lambda function store the result file in
    the same or a different S3 bucket, then check this
    cache here first for quick retrieval
    """
    req_phrase_file_content_decoded = b64decode(
        req_phrase_file_content_encoded)
    req_sound_file_content_decoded = b64decode(
        req_sound_file_content_encoded
    )

    phrase_file_path = _upload_to_s3(
        req_phrase_filename,
        req_phrase_file_content_decoded
    )

    sound_file_path = _upload_to_s3(
        req_sound_filename,
        req_sound_file_content_decoded
    )

    payload = {
        "phrase_file": phrase_file_path,
        "sound_file": sound_file_path
    }
    payload.update(kwargs)

    resp = requests.post(AWS_GATEWAY_URL, json=payload)
    response = resp.json()

    try:
        outputfile_decoded = BytesIO(b64decode(response["result_file"]))
        result_filename = (f"{req_phrase_filename}_{req_sound_filename}"
                           "_result.wav").lower()
        result_file_path = _upload_to_s3(result_filename, outputfile_decoded)
        exception = None
    except Exception as exc:
        print("ERROR", exc)
        result_file_path = None
        exception = str(exc)

    return phrase_file_path, sound_file_path, result_file_path, exception

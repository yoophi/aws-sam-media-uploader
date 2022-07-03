import logging
import os
import json

import boto3 as boto3

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

UPLOAD_BUCKET = os.environ.get("UPLOAD_BUCKET")
URL_EXPIRE_SECONDS = int(os.environ.get("URL_EXPIRE_SECONDS", 300))


def dict_to_path(params, *args, filename=None):
    prefix = [f"{k}:{params.pop(k)}" for k in args if k in params]
    suffix = sorted(params.items(), key=lambda x: x[0])
    path = "/".join(prefix + list(map(lambda x: ":".join(map(str, x)), suffix)))
    if filename:
        path = f"{path}/{filename}"

    return path


def lambda_handler(event, context):
    payload = json.loads(event.get("body", "{}"))
    filename = payload.pop("filename") if "filename" in payload else None
    path = dict_to_path(payload, filename=filename)

    s3 = boto3.client("s3")
    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": UPLOAD_BUCKET,
            "Key": path,
        },
        ExpiresIn=URL_EXPIRE_SECONDS,
    )

    body = json.dumps({"uploadUrl": presigned_url, "key": path})

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "http://localhost:3000"},
        "body": body,
    }

# Operaciones S3 — subida de archivos y listado de keys.

import boto3
from app.config import get_settings


def get_s3():
    s = get_settings()
    return boto3.client("s3", region_name=s.aws_region)


def upload_bytes(data: bytes, s3_key: str, content_type: str = "application/octet-stream") -> str:
    s = get_settings()
    key = f"{s.s3_prefix}/{s3_key}"
    get_s3().put_object(Bucket=s.s3_bucket_datalake, Key=key, Body=data, ContentType=content_type)
    return f"s3://{s.s3_bucket_datalake}/{key}"


def list_keys(prefix: str) -> list[str]:
    s = get_settings()
    full = f"{s.s3_prefix}/{prefix}"
    r = get_s3().list_objects_v2(Bucket=s.s3_bucket_datalake, Prefix=full, MaxKeys=100)
    return [o["Key"] for o in r.get("Contents", [])]

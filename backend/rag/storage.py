def download(self, key):
    obj = self.client.get_object(Bucket=self.bucket, Key=key)
    return obj["Body"].read()
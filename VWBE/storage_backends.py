from storages.backends.s3boto3 import S3Boto3Storage

class R2Storage(S3Boto3Storage):
    bucket_name = 'valourswealth'
    # endpoint_url = 'https://a5f9ee7b3883a9c77c46adca93821bec.r2.cloudflarestorage.com'
    endpoint_url = 'https://67216f1510b2341aed5462099561b745.r2.cloudflarestorage.com'
    file_overwrite = False

# https://67216f1510b2341aed5462099561b745.r2.cloudflarestorage.com/valourswealth

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# token name : valourswealth
# permission 3 : object read and write: allow the ability to read and write and list objects in specific buckets

# token : O9JEsKTEAhKF2gmES0eFT6RJ55gp0BIBmKbn4XIn
# access id : ea65d12791587a5f2e15788b7d34102a
# secret key: 0ffd08d2ca6ba6a777377fb64f698d2e011006491f9577004223128c5a3ae4fa
# s3 api endpoint url : https://67216f1510b2341aed5462099561b745.r2.cloudflarestorage.com


# then we go to the https://r2upload.cloud this website and launch a new app and added the info here and also copy the cors detail then
# now our app is ready for uploading and retrieveing details
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
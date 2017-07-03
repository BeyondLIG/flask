from nowstagram import app
from qiniu import Auth,put_data

#需要填写自己的access_key和secret_key
access_key=app.config['QINIU_ACCESS_KEY']
secret_key=app.config['QINIU_SECRET_KEY']

#构建鉴权对象
q=Auth(access_key,secret_key)

#要上传到的空间
bucket_name=app.config['QINIU_BUCKET_NAME']
domain_prefix=app.config['QINIU_DOMAIN']


def qiniu_upload_file(source_file,save_file_name):
    """upload_token生成上传凭证

    Args:
        bucket:  上传的空间名
        key:     上传的文件名，默认为空
        expires: 上传凭证的过期时间，默认为3600s
        policy:  上传策略，默认为空

    Returns:
        上传凭证
    """
    token=q.upload_token(bucket_name,save_file_name)


    """put_data上传二进制流到七牛

    Args:
        up_token:         上传凭证
        key:              上传文件名
        data:             上传二进制流
        params:           自定义变量，规格参考 http://developer.qiniu.com/docs/v6/api/overview/up/response/vars.html#xvar
        mime_type:        上传数据的mimeType
        check_crc:        是否校验crc32
        progress_handler: 上传进度

    Returns:
        一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
        一个ResponseInfo对象
    """
    ret,info=put_data(token,save_file_name,source_file.stream)

    print(type(info.status_code),info)
    if info.status_code==200:
        return domain_prefix+save_file_name
    return None
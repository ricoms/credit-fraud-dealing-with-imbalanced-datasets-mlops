# import base64
# import hashlib
# import os

# import falcon
# import pandas as pd
# import pytest

# from constants import MODULE_PATH


# @pytest.fixture()
# def training_data_dir():
#     data_dir = MODULE_PATH / 'api' / 'resources' / 'tests' / 'data'
#     assert data_dir.exists()
#     return data_dir


# @pytest.fixture()
# def data_filepath(training_data_dir):
#     return str(training_data_dir / 'training_set.parquet')


# @pytest.fixture()
# def encoded_training_data(data_filepath):
#     file_content = open(data_filepath, 'rb').read()
#     content = str(base64.urlsafe_b64encode(file_content), encoding='utf-8')
#     md5 = hashlib.md5(file_content).hexdigest()
#     yield data_filepath, content, md5


# def test_post_no_data_field(client):
#     headers = {
#         'content-type': 'application/parquet',
#     }

#     response = client.simulate_post(
#         '/score_data',
#         headers=headers
#     )
#     assert response.status == falcon.HTTP_BAD_REQUEST
#     assert response.json == {'error': 'Invalid payload.'}


# def test_post_wrong_header(client):
#     headers = {
#         'content-type': 'application/csv',
#     }

#     response = client.simulate_post(
#         '/score_data',
#         params=dict(content=123),
#         headers=headers
#     )
#     assert response.status == falcon.HTTP_BAD_REQUEST
#     assert response.json == {'error': 'File type not recognized.'}


# @pytest.mark.only
# def test_post(client, encoded_training_data):
#     origin_filepath, content, md5 = encoded_training_data

#     headers = {
#         'content-type': 'application/parquet',
#         'X-MD5': md5,
#         'Content-Disposition': 'attachment; filename=training_set.parquet'
#     }

#     payload = {
#         'filename': os.path.basename(origin_filepath),
#         'content': content,
#     }

#     response = client.simulate_post(
#         '/score_data',
#         params=payload,
#         headers=headers
#     )

#     assert response.status == falcon.HTTP_CREATED
#     assert 'path' in response.json
#     assert os.path.exists(response.json['path'])

#     upstream_filepath = response.json['path']
#     upstream_content = open(upstream_filepath, 'rb').read()

#     origin_content = open(origin_filepath, 'rb').read()
#     assert base64.decodebytes(upstream_content) == base64.decodebytes(origin_content)

#     pre_df = pd.read_parquet(origin_filepath)
#     post_df = pd.read_parquet(upstream_filepath)
#     assert all(pre_df == post_df)

#     os.remove(upstream_filepath)

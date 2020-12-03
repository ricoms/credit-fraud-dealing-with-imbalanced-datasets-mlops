# import math

# import falcon


# def test_post(client):
#     payload = {
#         "id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0",
#         "score_3": 480.0,
#         "score_4": 105.2,
#         "score_5": 0.8514,
#         "score_6": 94.2,
#         "income": 50000
#     }

#     response = client.simulate_post('/invocations', json=payload)

#     assert response.status == falcon.HTTP_OK


# def test_model(client):
#     payload = {
#         "id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0",
#         "score_3": 480.0,
#         "score_4": 105.2,
#         "score_5": 0.8514,
#         "score_6": 94.2,
#         "income": 50000
#     }

#     response = client.simulate_post('/invocations', json=payload)

#     answer = response.json
#     assert math.isclose(answer['prediction'], 0.1495, rel_tol=1e-2)
#     assert response.status == falcon.HTTP_OK

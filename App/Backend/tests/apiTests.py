def test_recommendation_topics():
    with app.test_client() as client:
        response = client.get('/recommendation_topics')
        print('Status Code:', response.status_code)
        print('JSON Response:', response.get_json())

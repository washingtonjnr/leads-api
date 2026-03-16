class TestHealthController:
    def test_health_check_success(self, client):
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_format(self, client):
        response = client.get("/health")
        
        data = response.json()
        
        assert isinstance(data, dict)
    
    def test_health_endpoint_accessible(self, client):
        response = client.get("/health")
        
        assert response.status_code in [200, 500]

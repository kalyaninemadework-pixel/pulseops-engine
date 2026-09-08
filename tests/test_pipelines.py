def get_auth_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "tester@pulseops.io",
        "username": "tester",
        "password": "testpass123",
        "full_name": "QA Engineer"
    })
    res = client.post("/api/v1/auth/login", data={"username": "tester", "password": "testpass123"})
    return res.json()["access_token"]

def test_ingest_telemetry_batch_with_anomaly_detection(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "pipeline_name": "Latency-Telemetry-Pipeline",
        "records": [
            {"metric_name": "api_latency_ms", "metric_value": 45.0},
            {"metric_name": "api_latency_ms", "metric_value": 48.0},
            {"metric_name": "api_latency_ms", "metric_value": 47.5},
            {"metric_name": "api_latency_ms", "metric_value": 46.2},
            {"metric_name": "api_latency_ms", "metric_value": 5000.0} # Outlier Anomaly
        ],
        "run_async": False
    }

    res = client.post("/api/v1/pipelines/ingest", json=payload, headers=headers)
    assert res.status_code == 202
    job_data = res.json()
    assert job_data["status"] == "COMPLETED"
    assert job_data["records_ingested"] == 5
    assert job_data["anomalies_detected"] >= 1

    # Verify Job Query
    job_id = job_data["id"]
    res_job = client.get(f"/api/v1/pipelines/jobs/{job_id}", headers=headers)
    assert res_job.status_code == 200
    assert res_job.json()["id"] == job_id

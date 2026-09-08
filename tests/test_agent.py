from tests.test_pipelines import get_auth_token

def test_genai_autonomous_root_cause_agent(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "pipeline_name": "Order-Processing-Stream",
        "records": [
            {"metric_name": "failed_tx_count", "metric_value": 2.0},
            {"metric_name": "failed_tx_count", "metric_value": 3.0},
            {"metric_name": "failed_tx_count", "metric_value": 1.0},
            {"metric_name": "failed_tx_count", "metric_value": 850.0}
        ]
    }
    ingest_res = client.post("/api/v1/pipelines/ingest", json=payload, headers=headers)
    job_id = ingest_res.json()["id"]

    # Trigger Autonomous AI Agent
    diag_res = client.post("/api/v1/agent/diagnose", json={"job_id": job_id}, headers=headers)
    assert diag_res.status_code == 200
    diag_data = diag_res.json()
    assert diag_data["job_id"] == job_id
    assert diag_data["status"] == "DIAGNOSED_AND_CONTAINED"
    assert len(diag_data["root_cause_summary"]) > 0
    assert len(diag_data["automated_remediation_plan"]) > 0

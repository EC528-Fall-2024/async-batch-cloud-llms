# Deploy Job Orchestrator on Cloud
gcloud functions deploy job-orchestrator \
    --region us-central1 \
    --runtime python312 \
    --timeout 540 \
    --memory 4Gi \
    --cpu 4 \
    --concurrency 1000 \
    --max-instances 1 \
    --source . \
    --entry-point start_job \
    --trigger-topic IncomingJob \
    --allow-unauthenticated 
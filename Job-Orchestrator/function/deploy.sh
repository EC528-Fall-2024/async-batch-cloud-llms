# Deploy Job Orchestrator on Cloud
gcloud functions deploy job-orchestrator \
    --region us-central1 \
    --runtime python312 \
    --timeout 540 \
    --memory 256Mi \
    --cpu 1 \
    --concurrency 1000 \
    --max-instances 10 \
    --source . \
    --entry-point start_job \
    --trigger-topic IncomingJob \
    --allow-unauthenticated 
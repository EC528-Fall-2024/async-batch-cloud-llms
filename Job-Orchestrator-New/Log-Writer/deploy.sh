# Deploy Log Writer on Cloud
gcloud functions deploy log-writer \
    --region us-central1 \
    --runtime python312 \
    --timeout 540 \
    --memory 256Mi \
    --cpu 1 \
    --concurrency 1000 \
    --max-instances 10 \
    --source . \
    --entry-point log \
    --trigger-topic Logs \
    --allow-unauthenticated 
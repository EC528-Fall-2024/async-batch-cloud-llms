# Deploy Status Writer on Cloud
gcloud functions deploy status-writer \
    --region us-central1 \
    --runtime python312 \
    --timeout 540 \
    --memory 4Gi \
    --cpu 4 \
    --concurrency 1000 \
    --max-instances 1 \
    --source . \
    --entry-point log \
    --trigger-topic Status \
    --allow-unauthenticated 
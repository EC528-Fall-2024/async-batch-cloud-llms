# Deploy Reverse Batch Processor on Cloud
gcloud functions deploy reverse-batch-processor \
    --region us-central1 \
    --runtime python312 \
    --timeout 540 \
    --memory 4Gi\
    --cpu 4 \
    --concurrency 1000 \
    --max-instances 1 \
    --source . \
    --entry-point reverse \
    --trigger-topic OutputData \
    --allow-unauthenticated \
    --service-account batch-processor@elated-scope-437703-h9.iam.gserviceaccount.com 
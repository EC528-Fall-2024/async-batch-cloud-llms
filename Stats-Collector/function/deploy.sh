# Deploy Stats Collector on Cloud
gcloud functions deploy stats-collector \
  --region us-central1 \
  --runtime python312 \
  --timeout 540 \
  --memory 4Gi \
  --cpu 4 \
  --concurrency 1000 \
  --max-instances 1 \
  --source . \
  --entry-point update \
  --trigger-topic Stats \
  --allow-unauthenticated 

# Manually select "Connect to VPC for outgoing traffic" under Networking for revision
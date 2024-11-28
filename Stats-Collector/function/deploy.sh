# Deploy Stats Collector on Cloud
gcloud functions deploy stats-collector \
  --region us-central1 \
  --runtime python312 \
  --timeout 540 \
  --memory 256Mi \
  --cpu 1 \
  --concurrency 1000 \
  --max-instances 10 \
  --source . \
  --entry-point update \
  --trigger-topic Stats \
  --allow-unauthenticated 

# Manually select "Connect to VPC for outgoing traffic" under Networking for revision
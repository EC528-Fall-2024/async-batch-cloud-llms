# push container to cloud
docker build -t rate-limiter .
docker tag rate-limiter gcr.io/elated-scope-437703-h9/rate-limiter
docker push gcr.io/elated-scope-437703-h9/rate-limiter

# deploy -- make sure to manually set CPU to always enabled
gcloud run deploy rate-limiter \
  --image gcr.io/elated-scope-437703-h9/rate-limiter \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 1 \
  --max-instances 1 \
  --timeout 3600 \
  --memory 512Mi \
  --cpu 1 \
  --concurrency 1000 \
  --network default
  
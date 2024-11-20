# Build the container
docker build -t flask-api .

# Tag the container for Google Container Registry
docker tag flask-api gcr.io/elated-scope-437703-h9/flask-api

# Push the container to GCR
docker push gcr.io/elated-scope-437703-h9/flask-api

# Deploy to Cloud Run
gcloud run deploy flask-api \
  --image gcr.io/elated-scope-437703-h9/flask-api \
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

# Deploy forward batch processor function
gcloud functions deploy batch-processor-http \
--runtime=python312 \
--region=us-central1 \
--timeout=540 \
--memory=256Mi \
--cpu=1 \
--concurrency=1000 \
--max-instances=10 \
--source=. \
--entry-point=go \
--trigger-http \
--allow-unauthenticated
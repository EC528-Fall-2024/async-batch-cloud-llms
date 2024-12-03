# Deploy forward batch processor function
gcloud functions deploy batch-processor-http \
--runtime=python312 \
--region=us-central1 \
--timeout=540 \
--memory=4Gi \
--cpu=4 \
--concurrency=1000 \
--max-instances=1 \
--source=. \
--entry-point=go \
--trigger-http \
--allow-unauthenticated \
--service-account=batch-processor@elated-scope-437703-h9.iam.gserviceaccount.com
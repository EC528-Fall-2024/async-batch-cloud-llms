# Deploy reverse batch processor function
gcloud functions deploy reverse-batch-processor \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--timeout=540 \
--memory=256Mi \
--cpu=1 \
--concurrency=1000 \
--max-instances=10 \
--source=. \
--entry-point=reverse \
--trigger-topic=OutputData \
--service-account=batch-processor@elated-scope-437703-h9.iam.gserviceaccount.com

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
--trigger-topic=OutputData

11:11
Got writing to datatable to work; have to set up non-free tier billing
Have to grant Job User or User to gserviceaccount (or other account/emails associated with this project that wants write access)
Job User/User status is a project-wide permission, there is 
SAMPLE_PROJ=$1
service_acc="batch-processor@elated-scope-437703-h9.iam.gserviceaccount.com"

gcloud config set project $SAMPLE_PROJ
gcloud services enable cloudresourcemanager.googleapis.com
gcloud auth application-default login
gcloud projects add-iam-policy-binding $SAMPLE_PROJ --member="serviceAccount:${service_acc}" --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding $SAMPLE_PROJ --member="serviceAccount:${service_acc}" --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding $SAMPLE_PROJ --member="serviceAccount:${service_acc}" --role="roles/bigquery.jobUser"

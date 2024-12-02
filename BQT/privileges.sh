#############

# Documentation:
# https://cloud.google.com/iam/docs/write-policy-client-libraries#client-libraries-usage-python

############

SAMPLE_PROJ="sampleproject-440900"
service_acc="dummy-account@elated-scope-437703-h9.iam.gserviceaccount.com"

gcloud config set project $SAMPLE_PROJ
gcloud services enable cloudresourcemanager.googleapis.com
gcloud auth application-default login
gcloud projects add-iam-policy-binding $SAMPLE_PROJ --member="serviceAccount:${service_acc}" --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding $SAMPLE_PROJ --member="serviceAccount:${service_acc}" --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding $SAMPLE_PROJ --member="serviceAccount:${service_acc}" --role="roles/bigquery.jobUser"

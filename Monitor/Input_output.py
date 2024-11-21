from flask import Flask, render_template, jsonify
from google.cloud import monitoring_v3
import os
import time
import pytz
from datetime import datetime

PROJECT_ID = "elated-scope-437703-h9"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "elated-scope-437703-h9-de7ac74c318d.json"

app = Flask(__name__)

boston_tz = pytz.timezone("America/New_York")


start_time_boston = boston_tz.localize(datetime(2024, 11, 19, 19, 0, 0))
end_time_boston = boston_tz.localize(datetime(2024, 11, 19, 20, 0, 0))


start_time_utc = start_time_boston.astimezone(pytz.utc)
end_time_utc = end_time_boston.astimezone(pytz.utc)

def fetch_pubsub_metrics():
    """Get Google Cloud Monitoring API metrics"""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"

    
    metrics_to_monitor = [
        {
            "name": "Input Data",
            "filter": 'metric.type = "pubsub.googleapis.com/topic/send_request_count" AND resource.labels.topic_id = "InputData"'
        },
        {
            "name": "Output Data",
            "filter": 'metric.type = "pubsub.googleapis.com/topic/send_request_count" AND resource.labels.topic_id = "OutputData"'
        },
    ]

   
    # interval = monitoring_v3.TimeInterval(
    #     {
    #         "end_time": {"seconds": int(time.time())},
    #         "start_time": {"seconds": int(time.time()) - 3600},  
    #     }
    # )

    interval = monitoring_v3.TimeInterval(
    {
        "start_time": {"seconds": int(start_time_utc.timestamp())},
        "end_time": {"seconds": int(end_time_utc.timestamp())},
    }
)

    metrics_data = {}
    for metric in metrics_to_monitor:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": metric["filter"],
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )

        
        data_points = []
        for result in results:
            resource_id = result.resource.labels.get("topic_id") or result.resource.labels.get("subscription_id")
            points = [
                {
                    "timestamp": point.interval.end_time.timestamp(),
                    "value": point.value.int64_value,
                }
                for point in result.points
            ]
            points.sort(key=lambda x: x["timestamp"])
            data_points.append({"resource_id": resource_id, "points": points})

        metrics_data[metric["name"]] = data_points

    return metrics_data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/metrics")
def get_metrics():
    metrics = fetch_pubsub_metrics()
    return jsonify(metrics)


if __name__ == "__main__":
    app.run(debug=True)

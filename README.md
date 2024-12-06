#  TurboBatch: Async Batch Processing Solution for Cloud-LLMs



## Team Members

| Names              | Roles   | Emails                |
| :----------------- | ------- | --------------------- |
| Yuhan Chen        | Student  | erv1n@bu.edu       |
| Noah Robitshek     | Student  | noahro@bu.edu      |
| Sergio Rodriguez      | Student  |  sergioer@bu.edu |
| Andrew Sasamori   | Student | sasamori@bu.edu        |
| Rayan Syed        | Student | rsyed@bu.edu         |
| Bennet Taylor     | Student | betaylor@bu.edu         |
| Stefan Philip | Mentor |        |
| Mayur Srivastava          | Mentor |       |

## Sprint Demo Videos:
[Sprint1 Demo](https://drive.google.com/file/d/1AckVEbBgkP-q0t7MMwMPyFpk_JpBOWmr/view?usp=sharing)  
[Sprint2 Demo](https://drive.google.com/file/d/1NjymlgsvtWI8tLfMjFaLiHEr-3TgZ8N5/view?usp=sharing)  
[Sprint3 Demo](https://drive.google.com/file/d/16_lV_df1BlzsAY3tFrf_6CKKA9yntzWA/view?usp=sharing)  
[Sprint4 Demo](https://drive.google.com/file/d/1QWUBAF8ekrdv3lGSUJAmf5UFGnswtPHv/view?usp=sharing)  
[Sprint5 Demo](https://drive.google.com/file/d/1RQ4_SbEfUcaeZkxm-eQ1F-HGWp4ByRd0/view?usp=sharing)  
Final Presentation


## Sprint Demo Slideshows:
[Sprint1 Slideshow](https://docs.google.com/presentation/d/14M9Q9WwM2tktHl2NyspCqJEftkKHSECiHJnucQ3VKqw/edit?usp=sharing)  
[Sprint2 Slideshow](https://docs.google.com/presentation/d/1h4vzF_IGO_7xRFhTZ4Gz1gRdLEJGcvXHZI2-pYbjRF4/edit?usp=sharing)   
[Sprint3 Slideshow](https://docs.google.com/presentation/d/1f_77tuTC3z717qgW_xtFdsB0G6VBBOTUwqp2TKolrZM/edit?usp=sharing)  
[Sprint4 Slideshow](https://docs.google.com/presentation/d/1LCoCL9HCC0GMx4awD1OfVJdlpK0LxsRrhhtyRrBAN9M/edit?usp=sharing)  
[Sprint5 Slideshow](https://docs.google.com/presentation/d/1nKVr_AxejMW-zizcu4_F4WmSpvvAdPP4nAIwX2-5RAw/edit?usp=sharing)  
Final Presentation Slideshow

## 1. The Problem

There are three large problems with the current process for calling LLMs available on the market. The first problem is Rate Limits which Cloud LLM providers impose. These limits prevent sending all requests simultaneously. Second is the problem of the Manual Oversight: required in the current process. The current manual process is inefficient and impractical for large-scale backfill jobs. The third problem is the inefficient management of requests caused a delayed timely output.


## 2.   Vision and Goals Of The Project:
The vision of this project is to create an automated, scalable, and efficient asynchronous batch processing solution for cloud-based Large Language Models (LLMs) at Two Sigma, enabling effortless data backfilling for large-scale financial datasets. By removing the complexity of rate limits imposed by cloud LLM providers and minimizing the need for manual oversight, this solution will allow for processing large amounts of data in an optimized and timely manner, ultimately improving operational capabilities.

High-Level Goals of this project include:
* Automating Rate-Limited Requests: Implement a queue system to manage the flow of LLM requests within the rate limits, making sure that millions of data points can be processed efficiently without intervention
* Optimize System Scalability and Efficiency: Architect the solution to handle large volumes of data and requests from multiple users, scaling dynamically while minimizing latency
* Improve User Experience: Develop a user-friendly interface for tracking the status of processing queues, monitoring system performance, and notifying users upon job completion
* Ensure Fault Tolerance: Design the system to gracefully handle failures, ensuring availability and reliability even under heavy workloads
* Cost Management: Optimize the use of cloud-based LLMs and other computational resources to minimize costs without sacrificing performance

## 3. Users/Personas Of The Project:

**Users**   
The users of this pipeline are traders at Two Sigma that want to run extremely large datasets through an LLM. They use this information to make trading divisions. Some examples could be news articles, financial documents, or weather data.  Speed and real time results are important to these traders. Additionally, having a low variable cost, or cost per job, is important. They should be able to monitor in-progress jobs, see completed jobs, and see errors that prevented a job from completing. The errors that a user sees should be user-friendly and all the information should be able to be viewed from a single UI (web-app or CLI)


**Operators**  
The operators of this pipeline are the development and operations employees at Two Sigma. They want a reliable system that can scale quickly. They want to have visibility into status/logs/errors from all jobs, machines, cloud functions. They would like easy access to information about the pipeline. Additionally, they would also like a single UI (web-app or CLI) that can allow them to see and configure all necessary data about the system.



## 4.   Scope and Features Of The Project:
**Scope Overview:**  

The scope of this project is to design and develop an asynchronous batch processing system that automates the management of rate limits and requests flows for cloud-based LLMs. The system will focus on ensuring efficient, scalable, and cost-effective processing of large datasets without requiring manual oversight. It will also provide a user-friendly interface for managing and monitoring the batch process along with an operator dashboard for operators to easily get insights on the system as a whole.

The solution will integrate with LLM providers (e.g. OpenAI) and streamline the communications across different APIs, ensuring a united approach to input and output BigQuery tables. The solution will provide users ways to check on job status, while automating key functions such as batch processing the input table, rate limiting the input prompts and data, and handling errors throughout the pipeline.

**In-Scope Features:** 
1. Async Batch Processing System:  
- Develop an asynchronous system that handles and processes large datasets efficiently through batching for cloud LLMs
- Enable the system to process tasks from multiple users and datasets at the same time
- Utilize Google PubSub for communication between all microservices within this system

2. Unified API Interface:
- Create a common interface between the backend and client-side for abstraction away from users and operators
- Allow job orchestrator to communicate with API to trigger the starting of the pipeline when needed
- Allow input via dataframes uploaded to BigQuery tables

3. Rate Limit Management:
- Implement automated handling of requests for LLMs through robust rate limiter keeping track of both requests and token usages with in-house tokenizer and rate-limiting algorithms with Redis for state
- Manage the flow of requests to the LLMs without requiring manual intervention, optimizing for speed and minimizing throttling
- Evaluate in-memory queues vs. persistent queues for optimal performance in handling large data backfill jobs

4. Scalability, Performance, and Cost Optimization:
- Design the system to scale horizontally, accommodating increasing workloads without degrading performance through the use of many serverless Google Cloud Functions
- Optimize resource use in cloud environments for cost management
- Implement monitoring tools to track resource usage and costs over time

**Stretch Features (Out-of-Scope for initial Phase):**
1. User Interface and Automation:
- Build a user-friendly interface in Jupyter Notebook to track and monitor the status of request, including the number of queued, processed, and completed tasks
- Present notifications to users when the process is complete or when issues arise

2. Advanced Analytics and Reporting
- Develop an analytics dashboard in Jupyter Notebook to provide insights into the system’s performance
- Capture and calculate key metrics such as LLM cost and throughput for operators to view overall performance and costs through the use of status writer and stats collector modules

This scope shows what was delivered in the project, focusing on asynchronous batch processing, scalability, and efficient rate limit management while avoiding unnecessary complexity and features in the initial development phases. However, the stretch quality-of-life features were also met successfully, providing users and operators an end-to-end robust pipeline with simple usability.

## 5. Solution Concept
![image](./images/Pipeline.jpg)

**Stage 1: User Interface/Operator Dashboards**  
The User Interface provides a clean interface for Users to set up their input/output BigQuery tables, upload their dataframes, and start their jobs with ease.
The Operator Dashboard provides operators an interface to monitor performance and retrieve core time and cost metrics regarding specific jobs and the pipeline as a whole. 
All metadata for both of the user personas’ dashboards are stored in the Firestore database throughout job execution and accessed through the Flask API as described in the subsequent sections.

**Stage 2: Information Digestion**  
![image](./images/FlaskAPI.jpg)
![image](./images/JobOrchestrator.jpg)
The start of the data pipeline will consist of collecting information from the users. Requests are packaged with metadata to be written into Firestore Database by the Job Orchestrator. The user’s data is uploaded as a BigQuery table which the system’s service account has access to. The request will then be sent to an HTTP endpoint exposed by our API hosted on google cloud. The API will then trigger the Job Orchestrator via the IncomingJob Pub/Sub topic, effectively starting the pipeline. 

**Stage 3: Batch Processing** 
![image](./images/BatchProcessor.jpg)
The Job Orchestrator will start the Batch Processor via an HTTP request containing relevant data for a user’s job. The Batch Processor will read from the input table in the user’s project in batches of 100, subsequently forwarding individual rows to the Rate Limiter via the InputData Pub/Sub Topic. Additionally, all important error information and time metrics are communicated to the Firestore database through Pub/Sub communication with the Status Writer and Stats Collector modules. 

**Stage 4: Rate Limiting** 
![image](./images/RateLimiter.jpg)
The Rate Limiter accepts input prompts and corresponding relevant text and uses an in-house tokenizer algorithm to predict the amount of tokens it will need. The prediction is used to dynamically allocate a user bucket for a specific client and subsequently attempt to retrieve tokens from a global bucket (depending on the model requested). Once tokens have been allocated the request passes through a request limiter (also depending on the model requested) before finally calling the LLM API and sending the response to the Reverse Batch Processor via the Pub/Sub OutputData Topic. Should a rate limit occur through the LLM API call, internal exponential backoff algorithms are performed. All token bucket and request limiting metadata is stored in Redis. Additionally, all important progress and error information along with relevant metrics are communicated to the Firestore database through Pub/Sub communication with the Status Writer and Stats Collector modules. 

**Stage 5: Reverse Batch Processor**
![image](./images/ReverseBatchProcessor.jpg)
The Reverse Batch Processor receives responses from the Rate Limiter and immediately writes them into the user’s project’s output BigQuery table for easy exporting as needed. Additionally, all important error information and time metrics are communicated to the Firestore database through Pub/Sub communication with the Status Writer and Stats Collector modules. 

## 6. Acceptance Criteria
Our minimum viable product will be labeled as:


Minimum Criteria
1. Ability to read data and write LLM responses to a cloud database.
2. Ensure compliance with rate limits and timely processing of large datasets.
3. Create a user interface for users to monitor the current jobs and completion status.


Stretch goals:
1. Implement advanced features such as dynamic rate limit adjustment based on real-time feedback from the LLM provider.
2. Develop analytics and reporting tools to provide insights into system performance and usage patterns.
3. Create a user interface for operators that allows for managing of pipeline load as well as monitor current clients and jobs in the pipeline. 
4. Develop logging infrastructure to comply with trading guidelines.
5. Handle alternative data types and formats include python DataFrames and pyarrow tables.



## 7. Rough Release Plan
**Sprint 1:** Research and Design 

During this sprint, we researched the different technologies and designed how our final product will function. 

**Sprint 2:** End to End Proof of Concept 

During this sprint, we built an end to end system that mocked the final data pipeline. This version did not use Redis and only implemented a basic version of Apache Kafka with an API call to the LLM.

**Sprint 3:** Cloud Implementation Redesign 

During this sprint, we applied the lessons learned from the end to end proof of concept and redesign our initial approach. In this sprint we transitioned away from Apache Kafka and Flink and moved towards a google Pub/Sub messaging application.

**Sprint 4:** Cloud Hosting of Functional elements 

During this sprint, we uploaded and tested many of the functional elements in the Google cloud. In this sprint we also redesigned and improved upon our architecture to adjust to the challenges we were experiencing. We moved many of the Cloud Run applications to Google Cloud Functions.

**Sprint 5:** End to End Cloud Implementation 

During this Sprint, we provided a full end to end functioning application with all pieces hosted on the Google Cloud. Additionally, basic performance metrics were implemented.

**Final Sprint:** Refactoring and Code Cleanup 

During this sprint, we worked on improving our performance and structure while refactoring and simplifying the implementations. User Interfaces and Operator Dashboards were created for efficient accessibility and ease of use.

## 8. Installation Guide

This guide provides a step-by-step process to set up the TurboBatch system, leveraging details from the README and the provided Jupyter Notebook.

### **Requirements**
1. **Environment Setup**:
    - A **Google Cloud Project** with an active billing account.
    - The **Google Cloud CLI** installed and authenticated on your machine.
    - Python (version 3.8 or higher)
   
2. **Dependencies**:
    - Install the required Python packages by running:
      ```bash
      pip install -r requirements.txt
      ```
    - Ensure that all dependencies listed in `requirements.txt` are installed in your environment.

---

### **Setup Steps**
#### Step 1: Configure Google Cloud
1. Create a Google Cloud project and link it to a billing account.
2. Authenticate and initialize the Google Cloud CLI:
   ```bash
   gcloud init
   gcloud auth login
   ```
3. Enable required APIs for your project:
   ```bash
   gcloud services enable pubsub.googleapis.com bigquery.googleapis.com cloudfunctions.googleapis.com
   ```

#### Step 2: Set Up Permissions
1. Navigate to the `helpers` directory in the repository.
2. Run the `privileges.sh` script to grant necessary permissions to the system's service account:
   ```bash
   ./privileges.sh [PROJECT_ID]
   ```
   Replace `[PROJECT_ID]` with your Google Cloud project ID.

---

### **Prepare Data**
1. Ensure your input data is formatted correctly:
    - The input file should have two columns:
      - `row`: Integer values.
      - `prompt_and_text`: Strings containing the data to be processed.
    - Example file: `example.csv`.

2. Use the provided helper function in the Jupyter Notebook to upload your dataset to BigQuery:
   ```python
   from helpers.df import CSV_to_BigQuery

   # Update these variables
   input_CSV_path = "example.csv"
   project_id = "your_project_id"
   dataset_id = "your_dataset_id"
   input_table_id = "input_table_name"
   output_table_id = "output_table_name"

   CSV_to_BigQuery(input_CSV_path, project_id, dataset_id, input_table_id, output_table_id)
   ```

---

### **Run the System**
1. Submit a job by running the appropriate cell in the Jupyter Notebook. Update the configuration variables as required.

2. Monitor your job's progress via the notebook interface. Updates on the job status will appear automatically.

---

### **Additional Notes**
- For advanced configuration or troubleshooting, refer to the helper scripts and modules in the repository.
- The `helpers` directory contains scripts like `privileges.sh` to streamline setup and management tasks.
- For a shorter guide, follow the instructions provided in the [UserNotebook](https://github.com/EC528-Fall-2024/async-batch-cloud-llms/blob/main/User-Script/UserNotebook.ipynb)

---

If you need assistance, feel free to share your questions!


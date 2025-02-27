# Current Version 1.0.4.dev (Still in Development)
* Add notes for next release here.

# Release 1.0.3
* Add API docs for Vertex Notification Email
* Add template JSON pipeline spec for running evaluation on a managed GCP Vertex model.
* Update documentation for Dataproc Serverless components v1.0.
* Use if:cond:then when specifying image name in built-in algorithm hyperparameter tuning job component and add separate hyperparameter tuning job default pipelines for TabNet and Wide & Deep
* Add gcp_resources in the eval component output
* Add downsampled_test_split_json to example_and_stats_gen component.

# Release 1.0.2
* Dataproc Serverless components v1.0 launch.
* Bump google-cloud-aiplatform version 
* Fix HP Tuning documentation, fixes #7460 
* Use feature ranking and selected features in AutoML Tables stage 1 tuning component.
* Update distill_skip_evaluation_pipeline for performance improvement.

# Release 1.0.1
* Add experimental email notification component
* add docs for create_custom_training_job_op_from_component
* Remove ForecastingTrainingWithExperimentsOp component.
* Use unmanaged_container_model for model_upload for AutoML Tables pipelines
* add nfs mount support for create_custom_training_job_op_from_component
* Implement cancellation for dataproc components
* bump google-api-core version to 2.0+
* Add retry for batch prediction component

# Release 1.0.0
* add enable_web_access for create_custom_training_job_op_from_component
* remove remove training_filter_split, validation_filter_split, test_filter_split from automl components
* Update the dataproc component docs

# Release 0.3.1
* Implement cancellation propagation
* Remove encryption key in input for BQ create model
* Add Dataproc Batch components
* Add AutoML Tables Wide & Deep trainer component and pipeline
* Create GCPC v1 and readthedocs for v1
* Fix bug when ExplanationMetadata.InputMetadata field is provided the batch prediction job component

# Release 0.3.0
* Update BQML export model input from string to artifact
* Move model/endpoint/job/bqml compoennts to 1.0 namespace
* Expose `enable_web_access` and `reserved_ip_ranges` for custom job component
* Add delete model and undeploy model components
* Add utility library for google artifacts

# Release 0.2.2
* Fixes for BQML components
* Add util functions for HP tuning components and update samples

# Release 0.2.1
* Add BigqueryQueryJobOp, BigqueryCreateModelJobOp, BigqueryExportModelJobOp and BigqueryPredictModelJobOp components
* Add ModelEvaluationOp component
* Accept UnmanagedContainerModel artifact in Batch Prediction component
* Add util components and fix YAML for HP Tuning Job component; delete lightweight python version
* Add generic custom training job component
* Fix Dataflow error log reporting and component sample

# Release 0.2.0
* Update custom job name to create_custom_training_job_op_from_component
* Remove special handling for "=" in remote runner.
* Bug fixes and documentation updates.

# Release 0.1.9
* Dataflow and wait components
* Bug fixes

# Release 0.1.8
* Update the CustomJob component interface, and rename to custom_training_job_op
* Define new artifact types for Google Cloud resources.
* Update the AI Platform components. Added the component YAML and uses the new Google artifact types
* Add Vertex notebook component
* Various doc updates

# Release 0.1.7
* Add support for labels in custom_job wrapper.
* Add a component that connects the forecasting preprocessing and training components.
* Write GCP_RESOURCE proto for the custom_job output.
* Expose Custom Job parameters Service Account, Network and CMEK via Custom Job wrapper.
* Increase KFP min version dependency.
* AUpdate documentations for GCPC components.
* Update typing checks to include Python3.6 deprecated types.

# Release 0.1.6
* Experimental component for Model Forecast.
* Fixed issue with parameter passing for Vertex AI components
* Simplify auto generated API docs
* Fix parameter passing for explainability on ModelUploadOp
* Update naming of project and location parameters for all for GCPC components

# Release 0.1.5
* Experimental component for vertex forecasting preprocessing and validation

# Release 0.1.4

* Experimental component for tfp_anomaly_detection.
* Experimental module for Custom Job Wrapper.
* Fix to include YAML files in PyPI package.
* Restructure the google_cloud_pipeline_components.

# Release 0.1.3

*   Use correct dataset type when passing dataset to CustomTraining.
*   Bump google-cloud-aiplatform to 1.1.1.

# Release 0.1.2

*   Add components for AutoMLForecasting.
*   Update API documentation.

# Release 0.1.1

*   Fix issue with latest version of KFP not accepting pipeline_root in kfp.compile.
*   Fix Compatibility with latest AI Platform name change to replace resource name class with Vertex AI

# Release 0.1.0

## First release

*   Initial release of the Python SDK with data and model managemnet operations for Image, Text, Tabular, and Video Data.

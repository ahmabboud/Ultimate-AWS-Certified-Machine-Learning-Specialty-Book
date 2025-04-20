# Simplified Hands-on Lab: Building a Basic CI/CD Pipeline for ML Models

## Lab Overview

This hands-on lab guides you through creating a simple CI/CD pipeline for machine learning models using AWS services. The lab is designed to be completed in under 30 minutes and focuses on core MLOps concepts without excessive technical complexity.

### Lab Objectives
- Set up a basic ML model CI/CD pipeline on AWS
- Understand key components of MLOps automation
- Implement automated model deployment
- Learn best practices for ML workflow automation

### Prerequisites
- AWS account with appropriate permissions
- Basic understanding of machine learning concepts
- Familiarity with AWS SageMaker

### Time Required
- Setup: 5 minutes
- Implementation: 20 minutes
- Cleanup: 5 minutes

## Lab Architecture

The lab implements a streamlined CI/CD pipeline with the following components:
1. **Source Repository**: AWS CodeCommit to store model code and configuration
2. **Build & Test**: AWS CodeBuild to run training and validation
3. **Model Registry**: Amazon SageMaker Model Registry to version models
4. **Deployment**: Amazon SageMaker for model deployment
5. **Monitoring**: Basic CloudWatch setup for endpoint monitoring

## Lab Steps

### Step 1: Set Up the Source Repository (5 minutes)
1. Create a CodeCommit repository named `mlops-lab-repo`
2. Clone the repository locally
3. Add the provided sample model files to the repository
4. Commit and push the files

### Step 2: Create the Build Project (5 minutes)
1. Create a CodeBuild project linked to the repository
2. Configure the build environment using the provided buildspec.yml
3. Set up necessary IAM permissions

### Step 3: Set Up SageMaker Model Registry (5 minutes)
1. Create a model group in SageMaker Model Registry
2. Configure model approval workflow
3. Set up model versioning

### Step 4: Create the Deployment Pipeline (5 minutes)
1. Create a CodePipeline pipeline with source and build stages
2. Add a deployment stage using SageMaker deployment actions
3. Configure the pipeline to trigger on repository changes

### Step 5: Test the Pipeline (5 minutes)
1. Make a simple change to the model hyperparameters
2. Commit and push the change to trigger the pipeline
3. Monitor the pipeline execution
4. Verify model deployment to SageMaker endpoint

### Step 6: Resource Cleanup (5 minutes)
1. Delete the SageMaker endpoint
2. Delete the CodePipeline pipeline
3. Delete the CodeBuild project
4. Delete the CodeCommit repository
5. Remove any IAM roles created for the lab

## Troubleshooting Tips

- **Pipeline Failure**: Check CodeBuild logs for specific error messages
- **Deployment Issues**: Verify IAM permissions for SageMaker deployment
- **Repository Access**: Ensure proper authentication for CodeCommit

## Lab Completion Checklist

- [ ] Successfully created CodeCommit repository with model code
- [ ] Configured CodeBuild project with appropriate buildspec
- [ ] Set up SageMaker Model Registry for versioning
- [ ] Created and tested the CI/CD pipeline
- [ ] Verified model deployment to SageMaker endpoint
- [ ] Completed all cleanup steps to avoid ongoing charges

## Best Practices

- Always implement proper resource cleanup after lab completion
- Use IAM roles with least privilege principles
- Consider implementing approval gates for production deployments
- Implement comprehensive testing before deployment
- Monitor deployed models for performance degradation

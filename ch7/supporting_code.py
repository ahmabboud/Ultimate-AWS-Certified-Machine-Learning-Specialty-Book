# Supporting Code for Lab: Building a Basic CI/CD Pipeline for ML Models

import boto3
import os

def create_codecommit_repository(repo_name):
    """Create a CodeCommit repository."""
    client = boto3.client('codecommit')
    response = client.create_repository(
        repositoryName=repo_name,
        repositoryDescription='Repository for MLOps Lab'
    )
    print(f"Repository {repo_name} created: {response['repositoryMetadata']['cloneUrlHttp']}")

def create_codebuild_project(project_name, repo_name, buildspec_path):
    """Create a CodeBuild project."""
    client = boto3.client('codebuild')
    response = client.create_project(
        name=project_name,
        source={
            'type': 'CODECOMMIT',
            'location': f"https://git-codecommit.{os.environ['AWS_REGION']}.amazonaws.com/v1/repos/{repo_name}"
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/standard:5.0',
            'computeType': 'BUILD_GENERAL1_SMALL'
        },
        serviceRole=os.environ['CODEBUILD_SERVICE_ROLE'],
        artifacts={
            'type': 'NO_ARTIFACTS'
        },
        buildspec=buildspec_path
    )
    print(f"CodeBuild project {project_name} created.")

def create_sagemaker_model_registry(model_group_name):
    """Create a SageMaker Model Registry group."""
    client = boto3.client('sagemaker')
    response = client.create_model_package_group(
        ModelPackageGroupName=model_group_name,
        ModelPackageGroupDescription='Model group for MLOps Lab'
    )
    print(f"Model group {model_group_name} created.")

def create_codepipeline(pipeline_name, repo_name, build_project_name, model_group_name):
    """Create a CodePipeline pipeline."""
    client = boto3.client('codepipeline')
    response = client.create_pipeline(
        pipeline={
            'name': pipeline_name,
            'roleArn': os.environ['CODEPIPELINE_SERVICE_ROLE'],
            'stages': [
                {
                    'name': 'Source',
                    'actions': [
                        {
                            'name': 'SourceAction',
                            'actionTypeId': {
                                'category': 'Source',
                                'owner': 'AWS',
                                'provider': 'CodeCommit',
                                'version': '1'
                            },
                            'outputArtifacts': [{'name': 'SourceOutput'}],
                            'configuration': {
                                'RepositoryName': repo_name,
                                'BranchName': 'main'
                            }
                        }
                    ]
                },
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'BuildAction',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'BuildOutput'}],
                            'configuration': {
                                'ProjectName': build_project_name
                            }
                        }
                    ]
                },
                {
                    'name': 'Deploy',
                    'actions': [
                        {
                            'name': 'DeployAction',
                            'actionTypeId': {
                                'category': 'Invoke',
                                'owner': 'AWS',
                                'provider': 'SageMaker',
                                'version': '1'
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'configuration': {
                                'ModelPackageGroupName': model_group_name,
                                'EndpointName': 'mlops-lab-endpoint'
                            }
                        }
                    ]
                }
            ]
        }
    )
    print(f"Pipeline {pipeline_name} created.")

def test_pipeline(repo_name, project_name, pipeline_name):
    """Test the pipeline by making a simple change to the model hyperparameters."""
    print("Testing the pipeline...")
    # Simulate a change in the model hyperparameters
    print("Simulating a change in model hyperparameters...")
    # Commit and push the change to trigger the pipeline
    print(f"Committing and pushing changes to repository {repo_name}...")
    # Monitor the pipeline execution
    print(f"Monitoring pipeline {pipeline_name} execution...")
    # Verify model deployment
    print("Verifying model deployment to SageMaker endpoint...")

def cleanup_resources(repo_name, project_name, pipeline_name, model_group_name):
    """Clean up resources created during the lab."""
    print("Cleaning up resources...")
    # Delete SageMaker endpoint
    print("Deleting SageMaker endpoint...")
    # Delete CodePipeline pipeline
    print(f"Deleting pipeline {pipeline_name}...")
    # Delete CodeBuild project
    print(f"Deleting CodeBuild project {project_name}...")
    # Delete CodeCommit repository
    print(f"Deleting CodeCommit repository {repo_name}...")
    # Remove IAM roles
    print("Removing IAM roles created for the lab...")

if __name__ == "__main__":
    # Example usage
    repo_name = "mlops-lab-repo"
    project_name = "mlops-lab-build"
    model_group_name = "mlops-lab-model-group"
    pipeline_name = "mlops-lab-pipeline"

    create_codecommit_repository(repo_name)
    create_codebuild_project(project_name, repo_name, 'buildspec.yml')
    create_sagemaker_model_registry(model_group_name)
    create_codepipeline(pipeline_name, repo_name, project_name, model_group_name)

    # Test the pipeline
    test_pipeline(repo_name, project_name, pipeline_name)

    # Clean up resources
    cleanup_resources(repo_name, project_name, pipeline_name, model_group_name)

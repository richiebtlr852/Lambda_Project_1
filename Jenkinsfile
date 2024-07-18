pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                // Clone the GitHub repository
                git 'https://github.com/yourusername/my-etl-project.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                dir('lambda') {
                    // Install dependencies
                    sh 'pip install -r requirements.txt -t .'
                }
            }
        }
        stage('Package Lambda') {
            steps {
                dir('lambda') {
                    // Package the Lambda function and dependencies into a ZIP file
                    sh 'zip -r9 ../lambda_function.zip .'
                }
            }
        }
        stage('Deploy Lambda') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials-id']]) {
                    // Deploy the ZIP file to AWS Lambda
                    sh 'aws lambda update-function-code --function-name your_lambda_function_name --zip-file fileb://lambda_function.zip'
                }
            }
        }
    }
}

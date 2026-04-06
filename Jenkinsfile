pipeline {
    agent any

    environment {
        PROJECT_DIR = "/opt/devops-project"
        JOB_NAME = "devops-job"
    }

    stages {

        stage('Start Minikube') {
            steps {
                sh 'minikube start --driver=docker || true'
            }
        }

        stage('Check Kubernetes') {
            steps {
                sh 'kubectl get nodes'
            }
        }

        stage('Delete Old Job') {
            steps {
                sh 'kubectl delete job $JOB_NAME || true'
            }
        }

        stage('Apply Job') {
            steps {
                sh '''
                cd $PROJECT_DIR
                kubectl apply -f job.yaml
                '''
            }
        }

        stage('Wait for Completion') {
            steps {
                sh 'kubectl wait --for=condition=complete job/$JOB_NAME --timeout=180s'
            }
        }

        stage('Check Pods') {
            steps {
                sh 'kubectl get pods'
            }
        }

        stage('Check Jobs') {
            steps {
                sh 'kubectl get jobs'
            }
        }

        stage('Logs') {
            steps {
                sh 'kubectl logs job/$JOB_NAME'
            }
        }
    }
}

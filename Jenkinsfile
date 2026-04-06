pipeline {
    agent any

    environment {
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        MINIKUBE_HOME = '/var/lib/jenkins/.minikube'
    }

    stages {

        stage('Start Minikube') {
            steps {
                sh '''
                export MINIKUBE_HOME=$MINIKUBE_HOME
                minikube start --driver=docker || true
                '''
            }
        }

        stage('Check Kubernetes') {
            steps {
                sh 'kubectl get nodes'
            }
        }

        stage('Delete Old Job') {
            steps {
                sh 'kubectl delete job devops-job --ignore-not-found'
            }
        }

        stage('Apply Job') {
            steps {
                sh 'kubectl apply -f /opt/devops-project/job.yaml'
            }
        }

        stage('Wait for Completion') {
            steps {
                sh 'kubectl wait --for=condition=complete job/devops-job --timeout=300s'
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
                sh 'kubectl logs job/devops-job'
            }
        }
    }
}

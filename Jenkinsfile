// Sweet Scoop CI/CD pipeline — ENSF final project
//
// Jenkins credentials this file expects (Manage Jenkins -> Credentials):
//   dockerhub        Username with password  (Docker Hub username + access token)
//   aws-credentials  Secret file             (AWS credentials file; for Learner Lab paste
//                                              the "AWS CLI" block from AWS Details)

pipeline {
    agent any

    // Stage 1: run when GitHub sends a push webhook
    triggers { githubPush() }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 45, unit: 'MINUTES')
    }

    environment {
        DOCKERHUB_USER = 'madiiha'
        IMAGE_TAG      = "${env.BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = 'sweetscoop-ci'
        STATE_DIR      = '/var/lib/jenkins/sweet-scoop'   // Terraform state + SSH key live here
        ANSIBLE_HOST_KEY_CHECKING = 'False'
    }

    stages {
        stage('1. Checkout (GitHub webhook on main)') {
            steps {
                checkout scm
                sh 'echo "Triggered by commit:" && git log -1 --pretty="%h %an: %s"'
            }
        }

        stage('2. Build') {
            steps {
                sh 'docker compose build backend frontend'
                sh 'docker images | grep sweet-scoop'
            }
        }

        stage('3. Automated Tests (Selenium)') {
            steps {
                sh 'APP_PORT=8081 docker compose up -d backend frontend'
                sh 'docker compose --profile test run --rm tests'
            }
            post {
                always { sh 'docker compose --profile test down --remove-orphans || true' }
            }
        }

        stage('4. Docker Image Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_TOKEN')]) {
                    sh '''
                        echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin
                        for svc in backend frontend; do
                          img="$DOCKERHUB_USER/sweet-scoop-$svc"
                          docker push "$img:$IMAGE_TAG"
                          docker tag  "$img:$IMAGE_TAG" "$img:latest"
                          docker push "$img:latest"
                        done
                        docker logout
                    '''
                }
            }
        }

        stage('5. Server Deployment (Terraform)') {
            steps {
                withCredentials([file(credentialsId: 'aws-credentials', variable: 'AWS_SHARED_CREDENTIALS_FILE')]) {
                    dir('terraform') {
                        sh '''
                            terraform init -input=false -reconfigure \
                              -backend-config="path=$STATE_DIR/terraform.tfstate"
                            terraform apply -auto-approve -input=false \
                              -var="key_path=$STATE_DIR/deploy-key.pem"
                            terraform output -raw public_ip > ../server_ip.txt
                            echo "Server IP: $(cat ../server_ip.txt)"
                        '''
                    }
                }
            }
        }

        stage('6. Server Configuration (Ansible)') {
            steps {
                sh '''
                    IP=$(cat server_ip.txt)
                    printf "[app]\\n%s ansible_user=ubuntu ansible_ssh_private_key_file=%s/deploy-key.pem\\n" \
                      "$IP" "$STATE_DIR" > ansible/inventory.ini
                    cat ansible/inventory.ini
                    ansible-playbook -i ansible/inventory.ini ansible/setup-server.yml
                '''
            }
        }

        stage('7. Container Execution') {
            steps {
                sh '''
                    ansible-playbook -i ansible/inventory.ini ansible/deploy-container.yml \
                      -e dockerhub_user=$DOCKERHUB_USER -e image_tag=$IMAGE_TAG
                    IP=$(cat server_ip.txt)
                    curl -sf "http://$IP/api/" && echo
                '''
            }
        }

        stage('8. Container Orchestration (Kubernetes)') {
            steps {
                sh '''
                    ansible-playbook -i ansible/inventory.ini ansible/deploy-k8s.yml \
                      -e dockerhub_user=$DOCKERHUB_USER -e image_tag=$IMAGE_TAG
                    IP=$(cat server_ip.txt)
                    curl -sf "http://$IP:30080/api/flavors" | head -c 200 && echo
                '''
            }
        }
    }

    post {
        success {
            sh '''
                IP=$(cat server_ip.txt 2>/dev/null || echo unknown)
                echo "Docker container:  http://$IP"
                echo "Kubernetes (k3s):  http://$IP:30080"
            '''
        }
    }
}

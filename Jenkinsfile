pipeline {
  agent any

  environment {
    DOCKER_COMPOSE = 'docker compose'
    SUCCESS_COLOR = '#00FF00'
    FAILURE_COLOR = '#FF0000'
    UNSTABLE_COLOR = '#FFFF00'
  }

  stages {
    stage('Build Image') {
      steps {
        sh 'docker build -t backend-geometria:latest .'
        echo 'Docker image backend-geometria:latest built successfully'
      }
    }
    
    stage('Test and Quality') {
      parallel {

        stage('[SQLITE] Unit Tests #2') {
          stages {
            stage('[SQLITE] #2 Run Unit Tests') {
              steps {

                script {
                  try {
                    echo 'Database service started in the background'
                    sh 'docker compose -f docker-compose3.yml run --remove-orphans unit'
                  } catch (Exception e) {
                    echo 'Unit tests failed to run'
                  }
                }

                //   echo 'Database service started in the background'
                // try {
                //   sh 'docker compose -f docker-compose3.yml run --remove-orphans unit'
                // } catch (Exception e) {
                //   unstable 'Unit tests failed to run'
                // }

              }
              // post {
              //   always {
                  
              //   //   script {
              //   // //junit 'reports/junit.xml'
              //   // junit testResults: 'reports/junit.xml', skipPublishingChecks: true


              //   // // publishHTML(
              //   // //   [allowMissing: false,
              //   // //   alwaysLinkToLastBuild: false,
              //   // //   keepAll: false,
              //   // //   reportDir: './reports/coverage',
              //   // //   reportFiles: 'index.html',
              //   // //   reportName: 'Coverage Report',
              //   // //   reportTitles: 'Coverage Report']
              //   // // )
              //   //   }

              //     // office365ConnectorSend webhookUrl: 'https://vzorsuite.webhook.office.com/webhookb2/fa7a83f6-cc5f-4a59-a44b-32cc2c6eaded@25dcca0b-680c-4cef-b276-d3d0ec1367af/JenkinsCI/7a8bec0e08bd4e62878250db7a28964c/4d6b34fe-3b39-4cea-bee6-7facb6183abf/V2nN3T7jKM7W-0oq3AxhXkj39td-brS0dIe2sqYLAvrOI1',
              //     //   message: 'Unit tests completed',
              //     //   status: currentBuild.result == 'SUCCESS' ? 'Success' : 'Failure'
              //   }
              // }
            }
          }
        }


        stage('[POSTGRESQL] Unit Tests') {
          stages {
            stage('[POSTGRESQL] Run Unit Tests') {
              steps {
                echo 'Database service started in the background'
//                sh 'docker compose -f docker-compose3.yml run --remove-orphans unit-postgresql'
                sh 'docker compose -f docker-compose3.yml -p unit-tests-postgres run --remove-orphans unit-postgresql'


              }
              post {

                //junit 'reports/junit.xml'

                always {
                  
                  script {
                junit testResults: 'reports/junit.xml', skipPublishingChecks: true


                publishHTML(
                  [allowMissing: false,
                  alwaysLinkToLastBuild: false,
                  keepAll: false,
                  reportDir: './reports/coverage',
                  reportFiles: 'index.html',
                  reportName: 'Coverage Report',
                  reportTitles: 'Coverage Report']
                )


                // sh 'docker compose -f docker-compose3.yml -p unit-tests-postgres down --remove-orphans'

                  }

                  // office365ConnectorSend webhookUrl: 'https://vzorsuite.webhook.office.com/webhookb2/fa7a83f6-cc5f-4a59-a44b-32cc2c6eaded@25dcca0b-680c-4cef-b276-d3d0ec1367af/JenkinsCI/7a8bec0e08bd4e62878250db7a28964c/4d6b34fe-3b39-4cea-bee6-7facb6183abf/V2nN3T7jKM7W-0oq3AxhXkj39td-brS0dIe2sqYLAvrOI1',
                  //   message: 'Unit tests completed',
                  //   status: currentBuild.result == 'SUCCESS' ? 'Success' : 'Failure'
                }
              }
            }
          }
        }
        
        // stage('Quality Checks') {
        //   stages {
        //     stage('Flake8') {
        //       steps {
        //         script {
        //           try {
        //             sh '${DOCKER_COMPOSE} -f docker-compose3.yml run --rm flake8'
        //             def flake8Output = sh(script: '''
        //               if [ -s reports/flake8.html ]; then
        //                 grep -c "E\\|F" reports/flake8.html || echo "0"
        //               else
        //                 echo "0"
        //               fi
        //             ''', returnStdout: true).trim()
        //             echo "Flake8 output: ${flake8Output}"
        //             def flake8Errors = 0
        //             try { flake8Errors = flake8Output.toInteger() } catch (e) { flake8Errors = 0 }
        //             if (flake8Errors > 0) {
        //               unstable "Flake8 found style errors. See report for details."
        //             }
        //           } catch (e) {
        //             echo "Error in Flake8: ${e}"
        //             unstable "Flake8 check encountered an error: ${e}"
        //           }
        //         }
        //       }
        //     }
        //     stage('Pylint') {
        //       steps {
        //         script {
        //           try {
        //             sh '${DOCKER_COMPOSE} -f docker-compose3.yml run --rm pylint'
        //             def pylintOutput = sh(script: '''
        //               if [ -s reports/pylint.html ]; then
        //                 grep -c "E:" reports/pylint.html || echo "0"
        //               else
        //                 echo "0"
        //               fi
        //             ''', returnStdout: true).trim()
        //             echo "Pylint output: ${pylintOutput}"
        //             def pylintErrors = 0
        //             try { pylintErrors = pylintOutput.toInteger() } catch (e) { pylintErrors = 0 }
        //             if (pylintErrors > 0) {
        //               unstable "Pylint found errors. See report for details."
        //             }
        //           } catch (e) {
        //             echo "Error in Pylint: ${e}"
        //             unstable "Pylint check encountered an error: ${e}"
        //           }
        //         }
        //       }
        //     }
        //     stage('Black') {
        //       steps {
        //         script {
        //           try {
        //             sh '${DOCKER_COMPOSE} -f docker-compose3.yml run --rm black'
        //             def blackOutput = sh(script: '''
        //               if [ -s reports/black.html ]; then
        //                 grep -c "would reformat" reports/black.html || echo "0"
        //               else
        //                 echo "0"
        //               fi
        //             ''', returnStdout: true).trim()
        //             echo "Black output: ${blackOutput}"
        //             def blackErrors = 0
        //             try { blackErrors = blackOutput.toInteger() } catch (e) { blackErrors = 0 }
        //             if (blackErrors > 0) {
        //               unstable "Black found formatting issues. See report for details."
        //             }
        //           } catch (e) {
        //             echo "Error in Black: ${e}"
        //             unstable "Black check encountered an error: ${e}"
        //           }
        //         }
        //       }
        //     }
        //     stage('Isort') {
        //       steps {
        //         script {
        //           try {
        //             sh '${DOCKER_COMPOSE} -f docker-compose3.yml run --rm isort'
        //             def isortOutput = sh(script: '''
        //               if [ -s reports/isort.html ]; then
        //                 grep -c "Imports are incorrectly sorted" reports/isort.html || echo "0"
        //               else
        //                 echo "0"
        //               fi
        //             ''', returnStdout: true).trim()
        //             echo "Isort output: ${isortOutput}"
        //             def isortErrors = 0
        //             try { isortErrors = isortOutput.toInteger() } catch (e) { isortErrors = 0 }
        //             if (isortErrors > 0) {
        //               unstable "Isort found import sorting issues. See report for details."
        //             }
        //           } catch (e) {
        //             echo "Error in Isort: ${e}"
        //             unstable "Isort check encountered an error: ${e}"
        //           }
        //         }
        //       }
        //     }
        //     stage('Bandit') {
        //       steps {
        //         script {
        //           try {
        //             sh '${DOCKER_COMPOSE} -f docker-compose3.yml run --rm bandit'
        //             def banditOutput = sh(script: '''
        //               if [ -s reports/bandit.html ]; then
        //                 grep -c "HIGH" reports/bandit.html || echo "0"
        //               else
        //                 echo "0"
        //               fi
        //             ''', returnStdout: true).trim()
        //             echo "Bandit output: ${banditOutput}"
        //             def banditErrors = 0
        //             try { banditErrors = banditOutput.toInteger() } catch (e) { banditErrors = 0 }
        //             if (banditErrors > 0) {
        //               unstable "Bandit found security issues. See report for details."
        //             }
        //           } catch (e) {
        //             echo "Error in Bandit: ${e}"
        //             unstable "Bandit check encountered an error: ${e}"
        //           }
        //         }
        //       }
        //     }
        //     stage('Publish Quality Reports') {
        //       steps {
        //         script {
        //           sh '''
        //             echo "Contenido del directorio reports:"
        //             ls -la reports/
        //             echo "Contenido de los reportes:"
        //             // cat reports/flake8.html || echo "No hay reporte de Flake8"
        //             cat reports/pylint.html || echo "No hay reporte de Pylint"
        //             cat reports/black.html || echo "No hay reporte de Black"
        //             cat reports/isort.html || echo "No hay reporte de Isort"
        //             cat reports/bandit.html || echo "No hay reporte de Bandit"
        //           '''
        //           publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'reports', reportFiles: 'flake8.html', reportName: 'Flake8 Report', reportTitles: 'Flake8 Report'])
        //           publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'reports', reportFiles: 'pylint.html', reportName: 'Pylint Report', reportTitles: 'Pylint Report'])
        //           publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'reports', reportFiles: 'black.html', reportName: 'Black Report', reportTitles: 'Black Report'])
        //           publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'reports', reportFiles: 'isort.html', reportName: 'Isort Report', reportTitles: 'Isort Report'])
        //           publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'reports', reportFiles: 'bandit.html', reportName: 'Bandit Report', reportTitles: 'Bandit Report'])
        //         }
        //       }
        //     }
        //   }
        // }
      }
    }


  stage('CONSTRUIR IMAGEN TEST') {
      steps {
        sh 'docker build -f Dockerfile.test  . -t api-geometria-test:latest'
      }
    }
  stage('DESPLIEGUE IMAGEN TEST') {
      steps {
      // sh 'docker stack rm test'
      // sh 'sleep 20 '
      sh 'docker stack deploy -c stack-test.yaml api_geometria'
    //   sh 'docker service update --force api_geometria_api-geometria '
      //sh 'docker stack update --force api_geometria'
      //sh 'docker service update --force test_api'
      }
    }

  stage('CONSTRUIR IMAGEN PROD ') {
      steps {
        sh 'echo not building prod image yet'
        // sh 'docker build . -t api:latest'
      }
    }




  stage('DESPLIEGUE PROD') {
      steps {
        sh 'echo not deploying prod image yet'
        // sh 'docker stack deploy -c stack-backend.yaml prod'
      }
    }

  }

  post {
    // success {
    //   script {
    //     office365ConnectorSend(
    //       webhookUrl: 'https://vzorsuite.webhook.office.com/webhookb2/fa7a83f6-cc5f-4a59-a44b-32cc2c6eaded@25dcca0b-680c-4cef-b276-d3d0ec1367af/JenkinsCI/7a8bec0e08bd4e62878250db7a28964c/4d6b34fe-3b39-4cea-bee6-7facb6183abf/V2nN3T7jKM7W-0oq3AxhXkj39td-brS0dIe2sqYLAvrOI1',
    //       message: "Pipeline [${env.JOB_NAME} #${env.BUILD_NUMBER}] completed successfully!",
    //       status: 'Success',
    //       color: SUCCESS_COLOR
    //     )
    //   }
    // }
    // failure {
    //   script {
    //     office365ConnectorSend(
    //       webhookUrl: 'https://vzorsuite.webhook.office.com/webhookb2/fa7a83f6-cc5f-4a59-a44b-32cc2c6eaded@25dcca0b-680c-4cef-b276-d3d0ec1367af/JenkinsCI/7a8bec0e08bd4e62878250db7a28964c/4d6b34fe-3b39-4cea-bee6-7facb6183abf/V2nN3T7jKM7W-0oq3AxhXkj39td-brS0dIe2sqYLAvrOI1',
    //       message: "Pipeline [${env.JOB_NAME} #${env.BUILD_NUMBER}] failed!",
    //       status: 'Failure',
    //       color: FAILURE_COLOR
    //     )
    //   }
    // }
    // unstable {
    //   script {
    //     office365ConnectorSend(
    //       webhookUrl: 'https://vzorsuite.webhook.office.com/webhookb2/fa7a83f6-cc5f-4a59-a44b-32cc2c6eaded@25dcca0b-680c-4cef-b276-d3d0ec1367af/JenkinsCI/7a8bec0e08bd4e62878250db7a28964c/4d6b34fe-3b39-4cea-bee6-7facb6183abf/V2nN3T7jKM7W-0oq3AxhXkj39td-brS0dIe2sqYLAvrOI1',
    //       message: "Pipeline [${env.JOB_NAME} #${env.BUILD_NUMBER}] completed with code quality issues.",
    //       status: 'Unstable',
    //       color: UNSTABLE_COLOR
    //     )
    //   }
    // }
    always {
      cleanWs()
    }
  }

  options {
    disableConcurrentBuilds()
  }
}
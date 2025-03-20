pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/DannyDan2016/Test-frontend-QA-Cod'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'npm install'
                bat 'npx playwright install'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat 'npx playwright test'
            }
        }
    }
}

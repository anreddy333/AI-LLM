pipeline {
    agent any

    environment {
        VENV_PATH = './venv'
        LLM_API_URL = 'http://10.1.148.59:5000/generate'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y curl python3-venv
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    ls
                    pip install --no-cache-dir -r requirements.txt
                    python -m playwright install --with-deps chromium
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    pytest tests/test_gmail_login.py --junitxml=test-results.xml >> build.log 2>&1 || exit 1
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test-results.xml,build.log', allowEmptyArchive: true
            cleanWs()
        }

        failure {
            script {
                def consoleLog = "No error details found in logs"
                try {
                    def buildLog = readFile('build.log')
                    def pipelineLog = currentBuild.rawBuild.getLog(1000).join('\n')

                    def errorLines = (buildLog + "\n" + pipelineLog).split('\n').findAll {
                        it.toLowerCase().contains('error') ||
                        it.toLowerCase().contains('fail') ||
                        it.toLowerCase().contains('exception') ||
                        it.toLowerCase().contains('not found') ||
                        it.toLowerCase().contains('fatal') ||
                        it.toLowerCase().contains('timeout') ||
                        it.toLowerCase().contains('refused') ||
                        it.toLowerCase().contains('cd:') ||
                        it.toLowerCase().contains('sudo') ||
                        it.toLowerCase().contains('exit code')
                    }

                    consoleLog = errorLines.take(50).join('\n')
                    if (consoleLog.length() > 5000) {
                        consoleLog = consoleLog.substring(0, 5000) + '\n[Log truncated]'
                    }
                } catch (e) {
                    consoleLog = "Error reading logs: ${e.message}"
                }

                def llmResponse = 'No response from LLM'
                try {
                    def promptText = """\
You are **BuildGPT**, a CI/CD and QA incident response specialist.

When given a Jenkins pipeline failure, you will:

1. **Locate** the failing **stage/step** (or report “UNKNOWN”).  
2. Summarize the **root cause** in ≤2 sentences.  
3. Provide **actionable fixes**—ordered, precise, and ready to execute.  
4. If a test snippet is provided, **review** it and:
   - Highlight the faulty line(s)
   - Suggest how to correct or harden the test  
5. Quote up to **5 log lines** as evidence.  
6. Offer “**Next Steps**” if the issue persists.

**Reply *exactly* in this Markdown template** (no extra text):

**Failure Stage**: <stage-name OR “UNKNOWN”>  
**Root Cause**: <one-sentence summary>

**Recommended Fix**:
1. <step 1>
2. <step 2>
3. <step 3>

**Key Evidence**:
${consoleLog}

**Test Code Review** _(none provided)_:

**Next Steps if Unresolved**:
- <idea 1>
- <idea 2>
"""

                    echo "Sending prompt to LLM..."
                    retry(3) {
                        def response = httpRequest(
                            url: "${env.LLM_API_URL}",
                            httpMode: 'POST',
                            contentType: 'APPLICATION_JSON',
                            requestBody: groovy.json.JsonOutput.toJson([
                                model: 'codellama',
                                prompt: promptText
                            ]),
                            validResponseCodes: '200:299',
                            timeout: 180,
                            consoleLogResponseBody: true
                        )
                        llmResponse = response.content ?: 'Empty response from LLM'
                        echo "Received LLM response:\n${llmResponse.take(300)}..."
                    }
                } catch (Exception e) {
                    llmResponse = "Error: Failed to contact LLM server - ${e.message}\n\nLog for manual triage:\n${consoleLog}"
                    echo "LLM error: ${e.message}"
                }

                writeFile file: 'llm-triage-result.txt', text: llmResponse
                sh "cat llm-triage-result.txt || echo 'Failed to read file'"
                archiveArtifacts artifacts: 'llm-triage-result.txt', allowEmptyArchive: true
            }
        }
    }
}
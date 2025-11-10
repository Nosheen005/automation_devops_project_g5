# Automation and devops - Group project
## Group 5

The purpose with this project is to build a DevOps pipeline from a simple python app to be deployed in Azure. 
![Pipeline overview](/assets/pipeline_overview.jpeg "Overview")

The overall architecture: 
1. API get request to Open Weatehr Map
2. Flask App with a simple UI to show today's weather in Stockholm
3. Test in Pytest
4. docker image being sent to docker Hub
5. Web App then deployed in Azure with link to Docker Hub

Step 1 to 3 is shared between team members, step 4 and 5 will be individually done in seperate forks.
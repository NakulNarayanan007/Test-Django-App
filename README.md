###install Docker
1. Get the latest Docker package

   ```    
        sudo apt-get install docker docker.io
        sudo apt-get install docker docker-engine 
   ```
       or

      ```  sudo apt-get install docker docker-machine ```
2. Add yourself to the docker group, log out, and then login back to ensure that you can run Docker commands without sudo:
 	``` sudo usermod -a -G docker $USER ```

3. Verify docker is installed correctly
      ``` sudo docker run hello-world ```

## Run locally

1.Clone the project to the local.


2.Move to the project folder path


3.To build Docker image for the  project, Run the following command
    ``` sudo docker build --tag image_name . ```
eg: sudo docker build --tag sample_app:1.0 .


4.Run a docker container with this image, By running this the app will be live.

   
eg:```sudo docker run --publish 8000:8000 --detach --name sample_app_container sample_app:1.0 ```


5.If you check the running Docker containers by using 
``` sudo docker ps ```.
 in here we can see our container running
  

6.Go to http:localhost:8000 in our browser their you can see our app live


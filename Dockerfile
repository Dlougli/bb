
#pulls python 3.7’s image from the docker hub 
FROM python:alpine3.7 
#copies the flask app into the container 
COPY . /app 
#sets the working directory 
WORKDIR /app 
#install each library written in requirements.txt 
RUN pip install -r requirements.txt  
#exposes port 8080 
EXPOSE 8080 
#Entrypoint and CMD together just execute the command  
#python app.py which runs this file 
ENTRYPOINT [ "python" ]  
CMD [ "app.py" ]  

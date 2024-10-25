This proxy folder will allow the frontend server to connect directly to the backend

it is done by doing a proxyreverse which allows a url to put in and then interpretted another way within docker

This is a apache run docker container that just runs on localhost 

To run this you need to do the following commands into your terminal

docker-compose -f docker-compose.local.yml up

then you need to docker-compose in another tab for the other conatiners web, service, and db.
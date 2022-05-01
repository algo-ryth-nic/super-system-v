FROM node 

# update the system
RUN apt-get update

# need this for py code
RUN apt-get install python pip -y

# make a dir where we store all our source code
RUN mkdir -p /home/app

# Copy all source code
WORKDIR /home/app
COPY ./node-server ./node-server
COPY ./python-related ./python-related
COPY ./react-client ./react-client
COPY ./requirements.txt ./requirements.txt

# Install Python requirments
RUN pip install -r requirements.txt

# build react app
WORKDIR /home/app/react-client
RUN npm install
RUN npm run build

# copy the builds to node server public dir
RUN cp -r /home/app/react-client/dist/* /home/app/node-server/public/

# Install modules for node server
WORKDIR /home/app/node-server
RUN npm install

# expose port 3000
EXPOSE 3000

# set node server as entrypoint
ENTRYPOINT npm start

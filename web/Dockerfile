# web/Dockerfile
FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install --save-dev prettier
RUN npm install react-dom
RUN npm install react-router-dom
RUN npm install recharts

COPY . .

EXPOSE 3000
CMD ["npm", "start"]


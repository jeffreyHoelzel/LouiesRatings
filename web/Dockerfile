# web/Dockerfile
FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install --save-dev prettier

COPY . .

EXPOSE 3000
CMD ["npm", "start"]


FROM node:16

WORKDIR /app

COPY package*.json ./
RUN npm install && \
    npm install --save-dev prettier react-dom react-router-dom recharts react-star-ratings && \
    npm install -g sass nodemon concurrently

COPY ./src/styles/ /app/src/styles/
COPY ./src/styles/components/ /app/src/styles/components/
COPY ./src/components/ /app/src/components/

RUN npm config set cache /app/.npm-cache

COPY . .


# Expose port and run the app along with the sass compiler
EXPOSE 3000
CMD ["npm", "start"]

FROM node:14

WORKDIR /app

COPY package*.json ./
RUN npm install && \
    npm install --save-dev prettier react-dom react-router-dom recharts react-star-ratings && \
    npm install -g sass


COPY ./src/styles/ /app/src/styles/
COPY ./src/components/ /app/src/components/


# Compile Sass to CSS
RUN sass /app/src/styles/main.scss /app/src/styles/main.css

COPY . .

# Expose port and run the app along with the sass compiler
EXPOSE 3000
CMD sass --watch /app/src/styles/main.scss:/app/src/styles/main.css & npm start

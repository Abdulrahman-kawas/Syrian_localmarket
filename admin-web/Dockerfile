# Build the admin SPA, then serve the static bundle with nginx.
FROM node:20-alpine AS build
WORKDIR /app

# Install deps first for better layer caching.
COPY package.json ./
RUN npm install

COPY . .
# API base URL is baked in at build time (override with --build-arg).
ARG VITE_API_URL=http://localhost:8000/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

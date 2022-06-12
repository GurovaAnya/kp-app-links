# build environment
FROM node:13.12.0-alpine as build
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
# production environment
FROM nginx:stable-alpine
#COPY /nginx/nginx.conf /nginx/nginx.conf
COPY /nginx/nginx.conf.template /nginx/nginx.conf.template
COPY --from=build /build /usr/share/nginx/html
#COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE $PORT
#CMD ["nginx", "-g", "daemon off;"]
CMD ["/bin/sh" , "-c" , "envsubst < /nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]
FROM nginx:latest

RUN mkdir -p /habit_tracker/staticfiles

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

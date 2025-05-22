#!/usr/bin/env sh
set -e

# Export API_URL so envsubst can use it
: ${API_URL:="http://api:8000"}
export API_URL

# `DEFAULT_HOST` is set by Webpack at container build time if the environment variable is provided.
# If this variable is not set at that time (like for production images), we must modify the rendered HTML on container up.
if [ -n "$DEFAULT_HOST" ]; then
    if sed -i -E "s/(<input[^>]*id=\"host\"[^>]*value=\")[^\"]*\"/\\1${DEFAULT_HOST}\"/" /usr/share/nginx/html/index.html; then
        echo "Updated DEFAULT_HOST value to $DEFAULT_HOST."
    else
        echo "An error occurred when attempting to set the DEFAULT_HOST value."
    fi
else
    echo "DEFAULT_HOST is not set. No changes made."
fi

# `DEFAULT_PORT` is set by Webpack at container build time if the environment variable is provided.
# If this variable is not set at that time (like for production images), we must modify the rendered HTML on container up.
if [ -n "$DEFAULT_PORT" ]; then
    if sed -i -E "s/(<input[^>]*id=\"port\"[^>]*value=\")[^\"]*\"/\\1${DEFAULT_PORT}\"/" /usr/share/nginx/html/index.html; then
        echo "Updated DEFAULT_PORT value to $DEFAULT_PORT."
    else
        echo "An error occurred when attempting to set the DEFAULT_PORT value."
    fi
else
    echo "DEFAULT_PORT is not set. No changes made."
fi

# Updates the `API_URL` variable in the Nginx config. Defaults to http://api:8000 if not set.
envsubst "\$API_URL" < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

exec nginx -g "daemon off;"

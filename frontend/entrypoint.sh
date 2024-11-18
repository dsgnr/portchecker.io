#!/usr/bin/env sh
set -e

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

exec nginx -g "daemon off;"

FROM node:25.9.0-alpine

# Upgrade system packages for security
RUN apk update && apk upgrade

# Create app directory owned by node user
RUN mkdir -p /app && chown -R node:node /app

WORKDIR /app

# Switch to non-root user
USER node

# Copy package files and install dependencies
COPY --chown=node:node package*.json ./
RUN npm install

# Copy project files
COPY --chown=node:node . .

# Expose Vite's default port
EXPOSE 5173

# Run Vite with host 0.0.0.0 to allow external access
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

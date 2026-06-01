FROM node:20-slim

# Create a non-root user
RUN useradd -m -s /bin/bash runner

# Set working directory
WORKDIR /code

# Switch to non-root user
USER runner

# Run the node script
CMD ["node", "main.js"]

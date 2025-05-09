ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install --upgrade python-dotenv && \
    pip install streamlit pandas matplotlib plotly requests beautifulsoup4 && \
    pip install nltk supabase

# Install Poetry
# https://python-poetry.org/docs/#installing-with-the-official-installer
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    # https://python-poetry.org/docs/#installing-with-the-official-installer
    # Step 3, you have to add poetry to your PATH, which on UNIX is in
    # $HOME/.local/bin
    echo "export PATH=/root/.local/bin:$PATH" >> $HOME/.bashrc

# Install Node.js via nvm.
# git needed to install degit when needed.
RUN apt-get update && apt-get install -y curl git
# From https://nodejs.org/en/download

ENV NVM_DIR /root/.nvm

# Download and install nvm:
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
  # This loads nvm.
  . "$NVM_DIR/nvm.sh" && \
  # Download and install Node.js:
  nvm install 20

#RUN ls -la

# Copy application code
COPY ../ /app/

# Expose Streamlit port
EXPOSE 8501

# TODO: Consider uncommenting this once out of development.
# Command to run the application
#CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]


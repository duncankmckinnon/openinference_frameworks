#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting bootstrap process...${NC}"

# Check if Python 3 is installed
if ! command -v python3.12 &> /dev/null; then
    echo -e "${RED}Python 3.12 is not installed. Please install Python 3.12 first.${NC}"
    echo -e "${RED}On macOS, you can install it with the following command:${NC}"
    echo -e "${RED}brew install python@3.12${NC}"
    exit 1
fi

# Check if venv module is available
if ! python3.12 -c "import venv" &> /dev/null; then
    echo -e "${RED}Python venv module is not available. Please install python3.12-venv package.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${GREEN}Creating new virtual environment...${NC}"
    python3.12 -m venv .venv
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${GREEN}Upgrading pip...${NC}"
python3.12 -m pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}Installing requirements...${NC}"
    pip install -r requirements.txt
else
    echo -e "${RED}requirements.txt not found. Skipping requirements installation.${NC}"
fi

echo -e "${GREEN}Bootstrap completed successfully!${NC}"
echo -e "${GREEN}To activate the virtual environment, run: source .venv/bin/activate${NC}"

#!/bin/bash
 
# Function to install necessary packages
install_dependencies() {
    echo "Checking and installing dependencies..."
 
    # Update system package list
    sudo apt-get update -y
 
    # Install necessary system packages
    sudo apt-get install -y make gcc python3 python3-pip python3-venv || {
        echo "Error: Failed to install system dependencies."
        exit 1
    }
 
    # Install Python packages
    pip3 install --upgrade pip
    pip3 install biopython numpy || {
        echo "Error: Failed to install Python dependencies."
        exit 1
    }
 
    echo "All dependencies are installed."
}
 
# Workflow 1: Certifier Framework Workflow
if [ "$1" == "certifier" ]; then
    install_dependencies
 
    # Check if correct number of arguments are passed
    if [ "$#" -ne 4 ]; then
        echo "Usage: $0 certifier <workflow_name> <workflow_data_path> <workflow_output_path>"
        exit 1
    fi
 
    # Capture arguments
    WORKFLOW_NAME=$2
    DATA_PATH=$3
    OUTPUT_PATH=$4
 
    # Define directories
    BASE_DIR="$HOME/certifier_workflows"
    WORKFLOW_DIR="$BASE_DIR/$WORKFLOW_NAME"
    DATA_DIR="$WORKFLOW_DIR/data"
    OUTPUT_DIR="$WORKFLOW_DIR/output"
 
    # Create necessary directories
    mkdir -p "$WORKFLOW_DIR" "$DATA_DIR" "$OUTPUT_DIR"
 
    # Copy workflow data to the data directory
    cp "$DATA_PATH" "$DATA_DIR/" || { echo "Error: Failed to copy data to $DATA_DIR"; exit 1; }
 
    # Initialize Certifier Framework
    CERTIFIER_DIR="/home/ccuser/certifier-framework-for-confidential-computing"  # Update this path to your Certifier installation
    cd "$CERTIFIER_DIR/src" || { echo "Error: Certifier directory not found"; exit 1; }
 
    # Build and verify Certifier framework
    make -f certifier.mak clean
    make -f certifier.mak || { echo "Error: Certifier framework build failed"; exit 1; }
 
    # Compile utilities
    cd "$CERTIFIER_DIR/utilities" || { echo "Error: Utilities directory not found"; exit 1; }
    make -f cert_utility.mak || { echo "Error: Certifier utility build failed"; exit 1; }
 
    # Run Certifier policy utility for setup
    ./cert_utility.exe \
        --operation=generate-policy-key-and-test-keys \
        --policy_key_output_file="$WORKFLOW_DIR/policy_key_file.bin" \
        --policy_cert_output_file="$WORKFLOW_DIR/policy_cert_file.bin" || { echo "Error: Policy key generation failed"; exit 1; }
 
    # Execute the workflow
    WORKFLOW_SCRIPT="$WORKFLOW_DIR/${WORKFLOW_NAME}.py"
 
    if [ -f "$WORKFLOW_SCRIPT" ]; then
        echo "Executing workflow: $WORKFLOW_SCRIPT"
        python3 "$WORKFLOW_SCRIPT" "$DATA_DIR" "$OUTPUT_DIR" || { echo "Error: Workflow execution failed"; exit 1; }
    else
        echo "Error: Workflow script $WORKFLOW_SCRIPT not found"
        exit 1
    fi
 
    echo "Workflow execution complete. Results are stored in $OUTPUT_DIR"
 
# Workflow 2: Differential Privacy Workflow
elif [ "$1" == "privacy" ]; then
    install_dependencies
 
    # Check if correct number of arguments are passed
    if [ "$#" -ne 5 ]; then
        echo "Usage: $0 privacy <workflow_name> <data_file.fna> <output_directory> <privacy_param>"
        exit 1
    fi
 
    # Capture arguments
    WORKFLOW_NAME=$2
    DATA_FILE=$3
    OUTPUT_DIR=$4
    PRIVACY_PARAM=$5
 
    # Create directories
    WORKFLOW_DIR="${OUTPUT_DIR}/${WORKFLOW_NAME}"
    DATA_DIR="${WORKFLOW_DIR}/data"
    JSON_DIR="${WORKFLOW_DIR}/json"
 
    mkdir -p "$WORKFLOW_DIR" "$DATA_DIR" "$JSON_DIR"
 
    # Copy data to workflow data directory
    cp "$DATA_FILE" "$DATA_DIR"
 
    # Extract file name without extension
    BASE_NAME=$(basename "$DATA_FILE" .fna)
 
    # Define JSON output file
    JSON_FILE="${JSON_DIR}/${BASE_NAME}.json"
 
    # Python script to generate JSON file and apply Laplace mechanism
    python3 <<EOF
import json
from Bio import SeqIO
import numpy as np
 
# Read arguments
fasta_file = "${DATA_DIR}/${BASE_NAME}.fna"
json_file = "$JSON_FILE"
epsilon = float("$PRIVACY_PARAM")
 
# Parse fasta and generate JSON metadata
data = []
for record in SeqIO.parse(fasta_file, "fasta"):
    data.append({
        "ID": record.id,
        "Length": len(record.seq),
        "Description": record.description,
        "AnonymizedValue": 0  # Placeholder to be modified by Laplace mechanism
    })
 
# Apply Laplace mechanism
for item in data:
    noise = np.random.laplace(loc=0.5, scale=1.0/epsilon)  # Add Laplace noise
    item["AnonymizedValue"] = max(0, min(1, noise))  # Clamp values between 0 and 1
 
# Write to JSON file
with open(json_file, "w") as outfile:
    json.dump(data, outfile, indent=4)
EOF
 
    echo "Workflow ${WORKFLOW_NAME} completed. JSON file created at: $JSON_FILE"
 
else
    echo "Error: Invalid workflow type. Use 'certifier' or 'privacy'."
    exit 1
fi
#!/bin/bash

# Test script to verify the fix for the -h flag conflict

echo "Testing help option..."
python image_optimizer.py -h

echo -e "\nTesting with height parameter..."
python image_optimizer.py . -a 800 -v

echo -e "\nTest completed."
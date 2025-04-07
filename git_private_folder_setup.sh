#!/bin/bash

# Step 1: Create private_folder (only if it doesn't already exist)
echo "Checking if private_folder exists..."
if [ ! -d "private_folder" ]; then
    echo "Creating private_folder..."
    mkdir private_folder
else
    echo "private_folder already exists."
fi

# Step 2: Create or update .gitignore to ignore private_folder
echo "Creating or updating .gitignore to ignore private_folder..."
if [ ! -f .gitignore ]; then
    touch .gitignore
    echo "Created .gitignore file"
fi

# Add private_folder to .gitignore if not already present
if ! grep -q "private_folder/" .gitignore; then
    echo "private_folder/" >> .gitignore
    echo "Added 'private_folder/' to .gitignore"
else
    echo "'private_folder/' already exists in .gitignore"
fi

# Step 3: Open .gitignore to edit manually if needed
echo "If you need to edit .gitignore, press Enter to open it in nano..."
read -p "Press Enter to open .gitignore in nano, or type 'skip' to skip editing: " edit_choice
if [ "$edit_choice" != "skip" ]; then
    nano .gitignore
fi

# Step 4: Remove files from Git's tracking (if they were already committed)
echo "Removing private_folder from Git's tracking if previously committed..."
git rm --cached -r private_folder

# Step 5: Commit changes to Git
echo "Committing changes..."
git add .gitignore
git commit -m "Update .gitignore to ignore private_folder and stop tracking its contents"
git push origin main

echo "Script complete!"

# # to run the script
# ./git_private_folder_setup.sh

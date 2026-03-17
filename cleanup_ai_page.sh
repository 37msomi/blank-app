#!/bin/bash
# Cleanup script to remove AI_Job_Market page

echo "🗑️  Removing AI_Job_Market page..."
rm -f "pages/2_📊_AI_Job_Market.py"

if [ ! -f "pages/2_📊_AI_Job_Market.py" ]; then
    echo "✅ AI_Job_Market page deleted successfully"
else
    echo "❌ Failed to delete AI_Job_Market page"
    exit 1
fi

# Verify what pages remain
echo ""
echo "📁 Remaining pages:"
ls -1 pages/

# Commit changes
echo ""
echo "📤 Preparing git commit..."
git add -A
git commit -m "Remove AI_Job_Market page for Streamlit Cloud deployment"
git push origin main

echo ""
echo "✅ Done! Ready to deploy to Streamlit Cloud"
echo "📍 Next: Go to https://share.streamlit.io and deploy"

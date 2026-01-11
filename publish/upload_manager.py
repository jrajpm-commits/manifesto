import os
import json
import glob

# Configuration
# Set this to the folder where your browser downloads files, or move files here
DOWNLOAD_FOLDER = "." 

def process_uploads():
    print(f"📂 Scanning for upload metadata in: {os.path.abspath(DOWNLOAD_FOLDER)}")
    
    # Find all JSON metadata files
    metadata_files = glob.glob(os.path.join(DOWNLOAD_FOLDER, "*.json"))
    
    if not metadata_files:
        print("No metadata (.json) files found. Make sure 'Generate Metadata JSON' is checked in the generator.")
        return

    print(f"Found {len(metadata_files)} metadata files.\n")
    
    for meta_file in metadata_files:
        # Skip non-manifesto files if needed
        if "manifesto" not in meta_file and "stories" not in meta_file:
             continue

        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it looks like our metadata
            if "video_file" not in data:
                continue
            
            if data.get("upload_status") == "uploaded":
                print(f"✅ Already uploaded: {data['video_file']}")
                continue
                
            video_path = os.path.join(DOWNLOAD_FOLDER, data["video_file"])
            
            # Verify video exists
            if not os.path.exists(video_path):
                print(f"⚠️  Video missing for metadata: {data['video_file']}")
                continue
                
            # ---------------------------------------------------------
            # READY FOR UPLOAD
            # ---------------------------------------------------------
            print(f"🚀 READY TO UPLOAD: {data['video_file']}")
            print(f"   Platform:    {data.get('platform', 'Unknown').upper()}")
            print(f"   Title:       {data.get('title', 'No Title')}")
            print(f"   Description: {data.get('description', '')[:60]}...")
            print(f"   Tags:        {', '.join(data.get('tags', []))}")
            
            # Here you would call your actual upload API
            # e.g., upload_to_youtube(video_path, data['title'], data['description'])
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error processing {meta_file}: {e}")

if __name__ == "__main__":
    process_uploads()

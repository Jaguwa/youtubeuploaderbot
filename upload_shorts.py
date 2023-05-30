import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API credentials
API_KEY = 'x'
CLIENT_SECRET_FILE = 'x'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Folder path containing titles and descriptions
titles_folder = 'C:/x'  # Update the path to the correct titles folder
output_folder = 'C:/x'  # Update the path to the correct output folder

def get_authenticated_service():
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, title, description, video_file):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['YouTube', 'Shorts']
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)

    response_upload = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()

    response_status = response_upload['status']['uploadStatus']
    if response_status == 'uploaded':
        print(f'Successfully uploaded: {title}')
    else:
        print(f'Failed to upload: {title}')

def main():
    youtube = get_authenticated_service()

    # Iterate over the range of video numbers
    for video_number in range(1, 21):
        title_file = os.path.join(titles_folder, f'{video_number}.txt')
        video_file = os.path.join(output_folder, f'script{video_number}_upscaled{video_number}.mp4')

        # Check if the title file exists
        if os.path.isfile(title_file):
            # Read title and description from the text file
            with open(title_file, 'r') as file:
                title = file.readline().strip()
                description = file.read().strip()

            # Check if the video file exists and has the .mp4 extension
            if os.path.isfile(video_file) and video_file.lower().endswith('.mp4'):
                # Upload the video
                upload_video(youtube, title, description, video_file)
            else:
                print(f'Invalid video file: {video_file}')
        else:
            print(f'Invalid title file: {title_file}')

if __name__ == '__main__':
    main()
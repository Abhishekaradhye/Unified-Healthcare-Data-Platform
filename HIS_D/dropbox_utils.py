import dropbox

class DropboxUploader:
    def __init__(self, token: str):
        self.dbx = dropbox.Dropbox(token)

    def upload_file(self, local_path: str, dropbox_path: str):
        try:
            with open(local_path, "rb") as f:
                self.dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
            print(f"Uploaded '{local_path}' → Dropbox path '{dropbox_path}'")

        except Exception as e:
            print(f"Error uploading '{local_path}' → {e}")
            raise e

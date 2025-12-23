import { api } from "../api/client";

export default function UploadPanel() {
  const upload = async (file: File) => {
    const form = new FormData();
    form.append("file", file);

    try {
      await api.post("/assets/upload/", form);
      alert(`Uploaded: ${file.name}`);
    } catch (err) {
      alert(`Upload failed: ${file.name}`);
    }
  };

  return (
    <div>
      <h3>Upload Files</h3>
      <input
        type="file"
        accept=".pdf,.docx,image/*"
        multiple
        onChange={(e) => {
          if (!e.target.files) return;
          Array.from(e.target.files).forEach(upload);
        }}
      />
    </div>
  );
}

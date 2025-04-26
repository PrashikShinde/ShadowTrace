import { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [scrapeResults, setScrapeResults] = useState([]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file)); // 🖼 show preview
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setUploading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage('Image uploaded successfully! ✅');
      console.log('Upload Response:', response.data);

      // After upload, trigger scraping
      const scrapeResponse = await axios.get('http://127.0.0.1:8000/scrape-results');
      console.log('Scrape Results:', scrapeResponse.data);
      if (scrapeResponse.data?.data?.results) {
        setScrapeResults(scrapeResponse.data.data.results);
      }
    } catch (error) {
      console.error(error);
      setMessage('Upload failed ❌. Please try again.');
    }
    setUploading(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">ShadowTrace - Upload Image</h1>

      {previewUrl && (
        <img
          src={previewUrl}
          alt="Preview"
          className="w-48 h-48 object-cover mb-4 rounded shadow-md"
        />
      )}

      <input
        type="file"
        onChange={handleFileChange}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        disabled={uploading}
        className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded shadow"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {message && (
        <div className="mt-4 text-lg font-semibold text-gray-700">
          {message}
        </div>
      )}

      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 w-full max-w-6xl">
        {scrapeResults.map((result, index) => (
          <div key={index} className="bg-white p-4 rounded shadow flex flex-col items-center">
            <img
              src={result.image_src}
              alt="Scraped Result"
              className="w-full h-48 object-cover mb-2 rounded"
            />
            <a
              href={result.page_link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline font-semibold"
            >
              Visit
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

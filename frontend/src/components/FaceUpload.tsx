"use client";

import React, { useState } from "react";
import axios from "axios";
import SearchResults from "./SearchResults";

const FaceUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setUploadResult(null);
    setMatches([]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const uploadResponse = await axios.post("http://localhost:8000/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      await axios.post("http://localhost:8000/scan/", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .then(res => console.log("Scan success:", res.data))
      .catch(err => console.error("Scan error:", err));


      // console.log("Scan Results: ", scanResponse.data);
      // setMatches(scanResponse.data.matches || []);
    } catch (err: any) {
      console.error("Upload/Scan Error:", err);
      setError("Failed to upload or scan image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-gray-900 rounded-2xl shadow-lg text-white space-y-6 mt-10">
      <h1 className="text-2xl font-bold text-center">Upload Face Image</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="block w-full text-white file:mr-4 file:py-2 file:px-4
        file:rounded-full file:border-0 file:text-sm file:font-semibold
        file:bg-blue-600 file:text-white hover:file:bg-blue-700"
      />

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded-xl w-full disabled:opacity-50 transition-all"
      >
        {loading ? "Uploading & Scanning..." : "Upload & Scan"}
      </button>

      {error && <p className="text-red-500 text-center">{error}</p>}

      {uploadResult && (
        <div className="text-sm bg-gray-800 p-4 rounded-xl">
          <p><strong>Upload:</strong> {uploadResult.message}</p>
          <p><strong>Filename:</strong> {uploadResult.filename}</p>
        </div>
      )}

      {matches.length > 0 && <SearchResults matches={matches} />}
    </div>
  );
};

export default FaceUpload;

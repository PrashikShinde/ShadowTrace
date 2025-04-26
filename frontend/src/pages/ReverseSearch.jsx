import { useState } from "react";
import axios from "axios";

export default function ReverseSearch() {
  const [message, setMessage] = useState("");

  const handleContinue = async () => {
    try {
      await axios.post("/api/reverse-search/continue");
      setMessage("Continuing scraping... 🕵️");
    } catch (error) {
      console.error(error);
      setMessage("Error continuing scraping ❌");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">🛡️ Solve CAPTCHA</h1>

      <div className="w-full max-w-6xl aspect-video border-2 border-gray-300 rounded-xl overflow-hidden shadow-md mb-6">
        <iframe
          src="http://localhost:9222/devtools/inspector.html"
          className="w-full h-full"
          title="Browser CAPTCHA"
        />
      </div>

      <button
        onClick={handleContinue}
        className="px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition"
      >
        Continue
      </button>

      {message && <p className="mt-4 text-green-700">{message}</p>}
    </div>
  );
}

import React, { useState } from "react";
import axios from "axios";
import { CardBody, CardContainer, CardItem } from "../components/ui/3d-card";
function UploadImage() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [uploadSuccess, setUploadSuccess] = useState(false);
    const [scrapeResults, setScrapeResults] = useState([]);

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };
    //   response.data.data.results[0].image_src
    const handleUpload = async () => {
        if (!selectedFile) return;
        setLoading(true);

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            await axios.post("http://127.0.0.1:8000/upload", formData);
            setUploadSuccess(true);

            // Now fetch the scrape results
            const response = await axios.get("http://127.0.0.1:8000/scrape-results");
            console.log("Scrape Results:", response.data);
            // Important: response.data.results
            setScrapeResults(response.data.data.results);
        } catch (error) {
            console.error("Error:", error);
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
            <h1 className="text-3xl font-bold mb-6">ShadowTrace - Upload Image</h1>

            <input type="file" onChange={handleFileChange} className="mb-4" />
            <button
                onClick={handleUpload}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded mb-6"
            >
                {loading ? "Uploading..." : "Upload"}
            </button>

            {uploadSuccess && (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 ">
                    {scrapeResults.map((result, index) => (
                        <div
                            key={index}
                            className="shadow-lg rounded-lg overflow-hidden  backdrop-blur-md z-10"
                        >

               

<CardContainer className="inter-var w-80 h-48">
      <CardBody className="bg-gray-50 relative group/card  dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border  ">
        <CardItem
          translateZ="50"
          className="text-lg text-center w-full font-bold text-gray-800 mt-8"
        >
          Output {index+1}
        </CardItem>
        {/* <CardItem
          as="p"
          translateZ="60"
          className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
        >
          Hover over this card to unleash the power of CSS perspective
        </CardItem> */}
        <CardItem translateZ="100" className="w-full mt-4">
            <center>
          <img
            src={result.image_src}
            className="w-56 h-48 object-fill z-30 rounded-lg"
            alt="thumbnail"
          />
            </center>
        </CardItem>
        <div className="flex justify-between items-center mt-6">
          <CardItem
            translateZ={20}
            as="a"
            href={result.page_link}
            target="__blank"
            className="px-4 py-2 rounded-xl w-full text-md text-center  text-blue-950 font-bold hover:underline"
          >
    Link→
          </CardItem>
          {/* <CardItem
            translateZ={20}
            as="button"
            className="px-4 py-2 rounded-xl bg-black dark:bg-white dark:text-black text-white text-xs font-bold"
          >
            Sign up
          </CardItem> */}
        </div>
      </CardBody>
    </CardContainer>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default UploadImage;

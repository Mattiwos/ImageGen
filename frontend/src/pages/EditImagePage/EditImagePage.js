import { useState } from 'react';
import axios from 'axios';

function EditImagePage() {
    const [prompt, setPrompt] = useState('');
    const [selectedFiles, setSelectedFile] = useState([]);
    const [pageState, setpageState] = useState('main')
    const [images, setImages] = useState([]);


    const handleDragOver = (event) => {
      event.preventDefault();
    };
  
    const handleDrop = (event) => {
      event.preventDefault();
      const files = event.dataTransfer.files;
      setSelectedFile(Array.from(files));
    };
    const handleFileChange = (event) => {
        const files = event.target.files;
     
        setSelectedFile(Array.from(files));
    };
    const handleRemoveFile =(index)=> {
      // console.log("remove: " + index);
      // console.log(selectedFiles);
      // setSelectedFile(selectedFiles.splice(selectedFiles.indexOf(index)));
      // console.log(selectedFiles);
      console.log(selectedFiles);
      setSelectedFile((prevFiles) => {
        const updatedFiles = [...prevFiles];
        updatedFiles.splice(index, 1);
        return updatedFiles;
      });
      //console.log(selectedFiles);
      
  
    };
    const handleUpload = () => {
        // You can implement your file upload logic here
        if (selectedFiles.length > 0) {
          // Example: send the file to a server
          const formData = new FormData();
          // Append each file to the FormData
          selectedFiles.forEach((file, index) => {
            formData.append(`file`, file);
          });
          formData.append('prompt',prompt);
    
          setpageState('loading');

          // Add your API call or upload logic here
          // For example using fetch or Axios
          axios.post(`${process.env.REACT_APP_BACKEND_URL}/editImage`, formData)
          .then(response => {
            return response.data;
          })
          .then(data => {
            setpageState('result');
            // Check if data.images is an array before calling map
            const imageUrls = Array.isArray(data.images) ? data.images.map(image => image.image_data) : [];
            setImages(imageUrls);
            setPrompt(data.prompt)
            // console.log(data);
            return data ? Promise.resolve(data) : Promise.resolve({});
        }).catch(error => {
            console.error('Error:', error);
            return Promise.reject(error);
          });


        }
      };
  
    return (
      <div className="bg-second min-h-screen from-gray-100 to-gray-300">

        <div className="scrollable-container">
            <div className="container py-10 px-10 mx-0 min-w-full flex flex-col items-center">
            <h1 className="mb-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-5xl lg:text-6xl"><span className="text-transparent bg-clip-text bg-gradient-to-r to-rose-600 from-lime-400">Edit Image</span></h1>
            </div>

        <br/>
        <br/>
        {/* <input type="file" onChange={handleFileChange} /> */}
          
      {pageState==="main" && (
        <div className="container py-10 px-10 mx-0 min-w-full flex flex-col items-center" onDrop={handleDrop} onDragOver={handleDragOver}>
          <label
            htmlFor="dropzone-file"
            className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
          >
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <svg
                className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 16"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                ></path>
              </svg>
              <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG, or GIF (MAX. 800x400px)</p>
            </div>
            <input
              id="dropzone-file"
              multiple
              type="file"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>
        
          {/* Display the list of selected files */}
          {selectedFiles.length > 0 && (selectedFiles.length > 0 && (
            <div>
              <h2 className="max-w-lg text-3xl font-semibold leading-normal text-gray-900 dark:text-white">Selected Files:</h2>
              <ul className="">
                {selectedFiles.map((file, index) => (
                  <li key={index}>
                    <span className="tracking-tighter text-gray-500 md:text-lg dark:text-gray-400">
                    {file.name}</span> - <button type="button" className="text-white bg-gradient-to-br from-green-400 to-blue-600 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-green-200 dark:focus:ring-green-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2" onClick={() => handleRemoveFile(index)}>
                    <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 20">
        <path d="M17 4h-4V2a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v2H1a1 1 0 0 0 0 2h1v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V6h1a1 1 0 1 0 0-2ZM7 2h4v2H7V2Zm1 14a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0v8Zm4 0a1 1 0 0 1-2 0V8a1 1 0 0 1 2 0v8Z"/>
      </svg></button>
                  </li>
                ))}
              </ul>
            </div>
          )) }


          <br/>

            <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
            Edit Prompt:</label>
            <input htmlFor="Caption" type="text" id="default-input" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" onChange={(e) => setPrompt(e.target.value)}/>
        
                  <br/>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded items-center" onClick={handleUpload}>
            Upload 
            </button>
          </div>
      )}
            {pageState==="loading" && (
        <div>


        <div className="text-center">
            <div role="status">
                  <svg aria-hidden="true" class="inline w-12 h-12 text-gray-200 animate-spin dark:text-gray-600 fill-pink-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                  <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
              </svg>
                <h3 className="text-white font-bold">Loading...</h3>
                <p className="text-white font-bold">This may take a few seconds, please don't close this page.</p>

            </div>
        </div>
        </div>
        
      )}

      {pageState==="result" && (
          <div>


        <div className="image-display text-center">
            
            <h3 className="text-white font-bold">Generated Image[s]:</h3>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {images.map((imageUrl, index) => (
                  <div>
                    <img className="h-auto max-w-full rounded-lg" key={index} alt={`Image ${index + 1}`} src={imageUrl} />
                  </div>
                ))
                }
            </div>  
            <h3 className="text-white font-bold">Prompt: {prompt}</h3>


              <br></br>
              <button className="inline-flex items-center justify-center bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded" onClick={() => setpageState('main')}>


                  <svg className="w-5 h-5 rtl:rotate-180" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 15.75L3 12m0 0l3.75-3.75M3 12h18" />
                  </svg>
                  <span> Back</span>
              </button>
        </div>
        </div>
        )}
      </div>
      
      </div>
    );
  }

  export default EditImagePage;



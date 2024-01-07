import React, { useEffect, useState } from "react";
import SideBar from "../SideBar/SideBar";
import {useNavigate} from 'react-router-dom';

function Home() {
    // const [open, setOpen] = useState(false);
    const [chatHistory, setChatHistory] = useState([]);
    const [isNewChat, setisNewChat] = useState(true)
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [documentId, setDocumentId] = useState(null);
    const [question, setQuestions] = useState([]);
    const [quiz, setQuiz] = useState([]);

    // const toggleDrawer = () => {
    //     setOpen(!open);
    // };


    const sendMessage = async (event) => {
        if (event.key === 'Enter') {
        const input = event.target;
        const message = input.value.trim();

        if (isNewChat) {
            console.log("Error: Upload a document to continue.");
            alert("Please upload a document before sending messages.");
            return; // Exit the function early if it's a new chat
        }

        if (message !== '') {
            setChatHistory([ ...chatHistory, message]);
            input.value = '';
        }
            try {
        const response = await fetch('http://127.0.0.1:8000/question/1/', {
            method: 'GET', // Assuming you want to retrieve data using GET
            headers: {
            'Content-Type': 'application/json',
            // Add any other headers as needed
            },
        });
    
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    
        const result = await response.json();
        setQuiz(result.summaries); // Update state with questions
        } catch (error) {
        console.error('Error fetching data from the backend:', error.message);
        }
        }
    };

    const Instructions = ["upload the document", "click Summarize", "You will get a summary of you document"]

    function handleFileUpload(event) {
        const fileInput = event.target;
        const selectedFile = fileInput.files[0];
        setisNewChat(false);
      
        if (selectedFile) {
            // Do something with the selected file, e.g., upload it to a server
            const formData = new FormData();
            formData.append('file', selectedFile);

            fetch('http://127.0.0.1:8000/upload/docupload/', {
            method: 'POST',
            body: formData,
            })
            .then(response => {
                if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Handle the response from the server
                 setDocumentId(data.Documentid);
                console.log('File uploaded successfully:', documentId);
                console.log('File uploaded successfully:', data);
                // You may want to perform additional actions with the response data

            })
            .catch(error => {
                // Handle errors more gracefully, e.g., display an error message
                console.error('Error uploading file:', error.message);
            });
        }
            

          console.log(`Selected file: ${selectedFile.name}`);
        
      }

      const handleLogout = () => { 
        localStorage.removeItem('token');
        navigate('/');
      }

      useEffect(() => {
        // Define an asynchronous function to fetch data
        const fetchData = async () => {
          try {
            // Make the asynchronous fetch request
            const response = await fetch(`http://127.0.0.1:8000/summarize/${documentId}/`);
            
            // Check if the request was successful
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
    
            // Parse the response JSON
            const result = await response.json();

    
            // Update the component state with the fetched data
            setData(result);
            console.log("Successuflly fetched data", result)
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        };
    
        // Call the async function
        fetchData();

        // Set up an interval to fetch data every, for example, 5 seconds (adjust as needed)
        
      }, [documentId]);

      const handleGenerateQuiz = async () => {
        try {
        const response = await fetch('http://127.0.0.1:8000/GenerateQuiz/1/', {
            method: 'GET', // Assuming you want to retrieve data using GET
            headers: {
            'Content-Type': 'application/json',
            // Add any other headers as needed
            },
        });
    
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    
        const result = await response.json();
        setQuestions(result.questions); // Update state with questions
        } catch (error) {
        console.error('Error fetching data from the backend:', error.message);
        }
    }


      
    return (
        <>
        <div className="relative">
                {/*logout button8*/}
                <button className="Btn mt-2" onClick={handleLogout}>
                
                    <div className="sign"><svg viewBox="0 0 512 512"><path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"></path></svg></div>
                    
                    <div className="text">Logout</div>
                </button>
                
                    {/*history button*/}
                   <div className="flex items-start">
                    <button
                    title="New Chat"
                    className="group ml-2 mt-2 cursor-pointer outline-none hover:rotate-90 duration-300"
                    onClick={() => setisNewChat(true)}
                    >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="50px"
                        height="50px"
                        viewBox="0 0 24 24"
                        className="stroke-white fill-none group-hover:fill-zinc-800 group-active:stroke-zinc-200 group-active:fill-zinc-600 group-active:duration-0 duration-300"
                    >
                        <path
                        d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z"
                        stroke-width="1.5"
                        fill="#011F43"
                        stroke="transparent"
                        ></path>
                        <path d="M8 12H16" stroke-width="1.5"></path>
                        <path d="M12 16V8" stroke-width="1.5"></path>
                    </svg>
                    </button>
                    </div>

                    
            
                    <br/>
                    <div className="z-10 mt-2">
                        <SideBar chatHistory={chatHistory}/>
                    </div>
                
        
        <h1 className="absolute top-2 left-[50%] font-bold h-16 bg-clip-text text-5xl text-white">Kuizdoc</h1>
        
       
            
            <div className="glass-effect absolute top-32  right-10 w-[60vw] h-[70vh] bg-transparent rounded-lg">
            { isNewChat ? (
            <div className="text-[#011F43] h-full w-full p-[5vw] glass-effect rounded-lg">
                <h1 className="text-center text-6xl font-bold">Welcome to Kuizdoc</h1>
                
                <div className="mt-20">
                    <h3 className="text-left text-2xl font-bold">Instructions</h3>
                    <ol className="list-decimal p-0 m-0">
                        {Instructions.map((item, index) => (
                            <li key={index} className="text-left text-2xl">
                            {item}
                            </li>
                        ))}
                    </ol>
                </div>

                <div>
                <div className="relative mx-auto w-[27%] cursor-pointer">
                    <label for="fileInput" className="cssbuttons-io-button cursor-pointer mx-auto mt-10 bg-[#011F43]">
                        <svg viewBox="0 0 640 512" fill="white" height="1em" xmlns="http://www.w3.org/2000/svg">
                        <path d="M144 480C64.5 480 0 415.5 0 336c0-62.8 40.2-116.2 96.2-135.9c-.1-2.7-.2-5.4-.2-8.1c0-88.4 71.6-160 160-160c59.3 0 111 32.2 138.7 80.2C409.9 102 428.3 96 448 96c53 0 96 43 96 96c0 12.2-2.3 23.8-6.4 34.6C596 238.4 640 290.1 640 352c0 70.7-57.3 128-128 128H144zm79-217c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l39-39V392c0 13.3 10.7 24 24 24s24-10.7 24-24V257.9l39 39c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-80-80c-9.4-9.4-24.6-9.4-33.9 0l-80 80z"></path>
                        </svg>
                        <span>Upload</span>
                    </label>
                    <input
                        type="file"
                        id="fileInput"
                        className="absolute top-0 left-0 opacity-0 w-[27%] h-full cursor-pointer"
                        onChange={(event) => handleFileUpload(event)}
                    />
                </div>

                </div>

                <p className="absolute bottom-4">Did you know you ask me anything from the document you have to upload?</p>

            </div>

            ) : (
                <>
                <div className="text-[#011F43]  w-full p-[vw] glass-effect rounded-lg">
                     <h2 className="text-2xl font-bold mt-1">Summaries:</h2>
                            <ul>
                                {data && data.summaries.map((summary, index) => (
                                    <li key={index}>{summary}</li>
                                ))}
                            </ul>
                 
                            </div>
                 
                <div className="text-[#011F43]  w-full p-[5vw] glass-effect rounded-lg">
                     <h2 className="text-2xl font-bold mt-1">Questions:</h2>
                            <ul>
                                {question && question.length >= 2 && question[1].map((summary, index) => (
                                    <li key={index}>{summary}</li>
                                ))}
                            </ul>
                 
                            </div>
                

                <div className="text-[#011F43]  w-full p-[5vw] glass-effect rounded-lg">
                     <h2 className="text-2xl font-bold mt-1">Answers:</h2>
                            <ul>
                                {quiz && quiz.length >= 2 && quiz[1].map((summary, index) => (
                                    <li key={index}>{summary}</li>
                                ))}
                            </ul>
                 
                            </div>
                </>

        
            )}
            {/* <input
                type="text"
                placeholder="Ask me anything..."
                onKeyDown={sendMessage}
                className=" w-full  p-2 mb-0 mt-10 block px-6 py-3 text-black bg-white border border-gray-200 rounded-full appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-[#011F43]"
            />
     <button onClick={sendMessage} className="ml-2 px-4 py-2 bg-blue-500 text-white">
    Send
  </button> */}
  <br/>
  <br/>
             <button className="summarize rounded-full float-right mb-5" onClick={handleGenerateQuiz}>
            <div className="svg-wrapper-1">
                <div className="svg-wrapper">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    width="14"
                    height="14"
                >
                    <path fill="none" d="M0 0h24v24H0z"></path>
                    <path
                    fill="currentColor"
                    d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z"
                    ></path>
                </svg>
                </div>
            </div>

            <span>Generate</span>
            </button>

            <br/>
            <div className="flex mt-10">

            <input
                type="text"
                placeholder="Type a message..."
                onKeyDown={sendMessage}
                className="p-2 mb-0 flex-grow my-auto block px-6 py-3 border border-gray-200 rounded-l-full appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-[#011F43]"
            />
            {/* <button onClick={sendMessage} className=" ">
                Send
            </button> */}
           
            
           
            <button className="button rounded-r-full" onClick={sendMessage}>
            <div className="svg-wrapper-1">
                <div className="svg-wrapper">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    width="14"
                    height="14"
                >
                    <path fill="none" d="M0 0h24v24H0z"></path>
                    <path
                    fill="currentColor"
                    d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z"
                    ></path>
                </svg>
                </div>
            </div>
            <span>Send</span>
            </button>

            </div>

            <p className="mt-4 text-center text-[#383DBB]">Kuizdoc may misinterprete your prompt. Consider cheking import information. </p>
            </div>
            
            </div>
            
                </>
            );
            }   

export default Home;

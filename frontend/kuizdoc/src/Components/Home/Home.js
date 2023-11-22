import React, { useState } from "react";
import SideBar from "../SideBar/SideBar";

function Home() {
    const [open, setOpen] = useState(false);
    const [chatHistory, setChatHistory] = useState([]);

    const toggleDrawer = () => {
        setOpen(!open);
    };

    const sendMessage = (event) => {
        if (event.key === 'Enter') {
        const input = event.target;
        const message = input.value.trim();

        if (message !== '') {
            setChatHistory([ ...chatHistory, message]);
            input.value = '';
        }
        }
    };

    const Instructions = ["upload the document", "click Summarize", "You will get a summary of you document"]

    return (
        <>
        <div className="relative">
                {/*logout button8*/}
                <button className="Btn mt-2">
                
                    <div className="sign"><svg viewBox="0 0 512 512"><path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"></path></svg></div>
                    
                    <div className="text">Logout</div>
                </button>
                
                    {/*history button*/}
                   <div className="flex items-start">
                    <button
                    title="History"
                    className="group ml-2 mt-2 cursor-pointer outline-none hover:rotate-90 duration-300"
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
                <button className="cssbuttons-io-button mx-auto mt-10 bg-[#011F43]">
                    <svg viewBox="0 0 640 512" fill="white" height="1em" xmlns="http://www.w3.org/2000/svg"><path d="M144 480C64.5 480 0 415.5 0 336c0-62.8 40.2-116.2 96.2-135.9c-.1-2.7-.2-5.4-.2-8.1c0-88.4 71.6-160 160-160c59.3 0 111 32.2 138.7 80.2C409.9 102 428.3 96 448 96c53 0 96 43 96 96c0 12.2-2.3 23.8-6.4 34.6C596 238.4 640 290.1 640 352c0 70.7-57.3 128-128 128H144zm79-217c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l39-39V392c0 13.3 10.7 24 24 24s24-10.7 24-24V257.9l39 39c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-80-80c-9.4-9.4-24.6-9.4-33.9 0l-80 80z"></path></svg>
                    <span>Upload</span>
                </button>
                </div>

                <p className="absolute bottom-4">Did you know you ask me anything from the document you have to upload?</p>

            </div>
            {/* <input
                type="text"
                placeholder="Ask me anything..."
                onKeyDown={sendMessage}
                className=" w-full  p-2 mb-0 mt-10 block px-6 py-3 text-black bg-white border border-gray-200 rounded-full appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-[#011F43]"
            />
     <button onClick={sendMessage} className="ml-2 px-4 py-2 bg-blue-500 text-white">
    Send
  </button> */}
            <div className="flex">
            <input
                type="text"
                placeholder="Type a message..."
                onKeyDown={sendMessage}
                className="p-2 mb-0 flex-grow mt-10 block px-6 py-3 border border-gray-200 rounded-l appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-[#011F43]"
            />
            {/* <button onClick={sendMessage} className=" ">
                Send
            </button> */}
            <button className="button" onClick={sendMessage}>
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
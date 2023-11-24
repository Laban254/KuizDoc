import React, { useState } from 'react';


function SideBar({chatHistory}) {          
  return (
    <div class="container ">
        <div class="box ">
            <span class="title text-[#011F43] text-center">History</span> 
            <div>
            <ol id="chatHistory" className="list-decimal p-0 ml-10">
            {chatHistory.slice(0).reverse().map((message, index) => (
                <li key={index} className="text-left text-white p-2 cursor-pointer transition-bg hover:bg-[#011F43]">
                  {message}
                </li>
              ))}
              </ol>
        </div>
    </div>
    </div>
  );
}

export default SideBar;

import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';




function InputField({ label, id, type, onChange, value, options, isSignup, inputType, pattern }) {
  
    return (
      <div className="block relative">
        <label htmlFor={id} className="mt-4 block text-white cursor-text text-sm leading-[140%] font-normal mb-2">
          {label}
        </label>
        <input
          type={type}
          id={id}
          className="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2 ring-gray-900 outline-0"
          onChange={onChange}
          value={value}
          list={options}
          pattern={pattern}
          
        />
        {isSignup && !inputType && <div className="text-sm text-red-500 text-center">{`Please fill in your ${label}`}</div>}
      </div>
    );
  }

function FormSection({ title, subtitle, children, onSubmit }) {
    
    return (
      <div className="max-w-lg relative flex flex-col p-4 rounded-md bg-[#011329] text-white" >
        <div className="text-2xl font-bold mb-2 text-white text-center">{title}</div>
        <div className="text-sm font-normal mb-4 text-center text-white">{subtitle}</div>
        <form className="flex flex-col gap-3 flex-grow" onSubmit={onSubmit}>
          {children}
        </form>
      </div>
    );
}
  
function Auth() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSignup, setIsSignup] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [confirmEmail, setConfirmEmail] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const navigate = useNavigate();
  

    useEffect(() => {
        if (email && password) {
          setError("");
        }
       }, [email, password]);
    const handleLoginSubmit = (e) => {
      e.preventDefault();
       // Login Form validation
       if (!isSignup && !email || !password) {
        setError("Please fill in all fields");
        return;
      }
      navigate("/home")
    }

    const handleSignUpSubmit = (e) => {
        e.preventDefault();
    
       

        // Signup Form validation
       
        if (isSignup && !lastName) {
          setError("Please fill in your last name");
          return;
        }
        if (isSignup && !email) {
          setError("Please fill in your email");
          return;
        }
        if (isSignup && !confirmEmail) {
          setError("Please confirm your email");
          return;
        }
        if (isSignup && email !== confirmEmail) {
          setError("Email and Confirm Email do not match");
          return;
         }
         
        if (isSignup && !password) {
          setError("Please fill in your password");
          return;
        }
        if (isSignup && !confirmPassword) {
          setError("Please confirm your password");
          return;
        }

        if (isSignup && password !== confirmPassword) {
          setError("Password and Confirm Password do not match");
          return;
         }
         if (isSignup && age) {
          setError("Please fill in your age");
          return;
         }
         if (isSignup && !age) {
          setError("Please fill in your age");
          return;
         }
         



        // Successful login
        console.log(isSignup? "Signup sucessfull" : "Login successful!");
        setIsSignup(false)
        
      };

    return (
        <>
        {/** relative flex flex-col p-2 rounded-md bg-[#011F43]*/}
            <div className="flex flex-col items-center justify-center h-screen ">
                <div className="p-10 mx-auto rounded-md bg-[#011F43]">
                    <FormSection
                    title={isSignup? "Create your account" : "Welcome back to Kuizdoc"}
                    subtitle={isSignup? "Signup to create your account" : "Log in to your account"}
                    onSubmit={isSignup ? handleSignUpSubmit : handleLoginSubmit}
                    >
                      {isSignup ? (
                        <>
                        <div className="flex flex-wrap -mx-2 gap-x-6">
                          <InputField
                          label="First Name"
                          id="firstName"
                          type="text"
                          onChange={(event) => setFirstName(event.target.value)}
                          value={firstName}
                          className="w-full sm:w-1/2 px-2 mb-4"
                          rules={{ 
                            required: true, 
                            pattern: /^[A-Za-z]{1,10}$/
                          }} 
                          inputType={firstName}  
                          isSignup={isSignup}                    
                          />
                          
          

                          <InputField
                          label="Last Name"
                          id="lastName"
                          type="text"
                          onChange={(event) => setLastName(event.target.value)}
                          value={lastName}
                          className="w-full sm:w-1/2 px-2 mb-4"
                          rules={{ 
                            required: true, 
                            pattern: /^[A-Za-z]{1,10}$/
                          }}
                          inputType={lastName}  
                          isSignup={isSignup} 
                         
                          />

                          <InputField 
                          label="Email" 
                          id="email" 
                          type="text" 
                          onChange={(event) => setEmail(event.target.value)}
                          value={email}
                          className="w-full sm:w-1/2 px-2 mb-4"
                          rules={{ 
                            required: true, 
                            pattern: /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
                          }}
                          inputType={email}  
                          isSignup={isSignup} 
                          
                          />
                          


                          <InputField
                          label="Confirm Email"
                          id="confirmEmail"
                          type="text"
                          onChange={(event) => setConfirmEmail(event.target.value)}
                          value={confirmEmail}
                          className="w-full sm:w-1/2 px-2 mb-4"
                          inputType={confirmEmail}  
                          isSignup={isSignup} 
                          />
                         
                          <InputField 
                          label="Password" 
                          id="password" 
                          type="password" 
                          onChange={(event) => setPassword(event.target.value)}
                          value={password}
                          className="w-full sm:w-1/2 px-2 mb-4"
                          inputType={password}  
                          isSignup={isSignup} 
                          /> 

                          <InputField
                          label="Confirm Password"
                          id="confirmPassword"
                          type="password"
                          onChange={(event) => setConfirmPassword(event.target.value)}
                          value={confirmPassword}
                          className="w-full sm:w-1/2 px-2 mb-4"
                          inputType={confirmEmail}  
                          isSignup={isSignup} 
                          />
                          <div className=" w-full sm:w-1/2 mb-4 ml-0">
                            <label htmlFor="gender" className="mt-4 block text-white cursor-text text-sm leading-[140%] font-normal mb-2">
                              Gender
                              </label>
                              <select
                              id="gender"
                              className="rounded border border-gray-200 text-sm w-full  font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2 ring-gray-900 outline-0"
                              onChange={(event) => setGender(event.target.value)}
                              value={gender}
                              required
                              >
                              <option value="male">Male</option>
                              <option value="female">Female</option>
                              <option value="other">Other</option>
                              </select>

                          </div>

                            <InputField
                            label="Age"
                            id="age"
                            type="date"
                            onChange={(event) => setAge(event.target.value)}
                            value={age}
                            inputType={age}  
                            isSignup={isSignup} 
                            className="w-full sm:w-1/2 px-2 mb-4"
                            />
                            </div>
                          
                        </>
                      ) : (
                        <>
                        <InputField 
                        label="Email" 
                        id="email" 
                        type="text" 
                        onChange={(event) => setEmail(event.target.value)}
                        value={email}/>

                        <InputField 
                        label="Password" 
                        id="password" 
                        type="password" 
                        onChange={(event) => setPassword(event.target.value)}
                        value={password}/>
                        </> 
                        )}   

                        
                        <div>
                            <a className="text-sm text-[#77CAFF]" href="#">
                            {isSignup? "": "Forgot your password?"}
                            </a>
                        </div>
                        <button type="submit" className="bg-[#77CAFF] w-48 m-auto px-1 py-3 rounded text-white text-md font-normal">
                            {isSignup ? "Sign up" : "Log in"}
                        </button>
                    </FormSection>
                    <button onClick={() => setIsSignup(!isSignup)} className="text-sm text-[#77CAFF]">
                    {isSignup ? "Already have an account? Log in" : "Don’t have an account yet? Sign up for free!"}
                    </button>
                </div>
            </div>
        </>
    );
}

export default Auth;
import React from 'react';

const Hero = () => {
  return (
    <div>
        <div className="hero min-h-screen mb-10 " >
            <div className="hero-content text-center text-neutral-content">
                <div className="max-w-md">
                <h1 className=" text-5xl font-bold">VOYAGER PRO</h1>
                <p className="mb-5 text-sm text-amber-400"> Powered by Gemini</p>
                <p className="mb-5 text-2xl ">Where your dreams of travelling abroad come to life</p>
                <a href='/generator'>
                  <div class="w-full h-40 flex items-center justify-center cursor-pointer">
                    <div
                      class="relative inline-flex items-center justify-start py-3 pl-4 pr-12 overflow-hidden font-semibold shadow text-amber-400 transition-all duration-150 ease-in-out rounded hover:pl-10 hover:pr-6 bg-gray-50 dark:bg-gray-700 dark:text-white dark:hover:text-gray-200 dark:shadow-none group"
                    >
                      <span
                        class="absolute bottom-0 left-0 w-full h-1 transition-all duration-150 ease-in-out bg-yellow-600 group-hover:h-full"
                      ></span>
                      <span
                        class="absolute right-0 pr-4 duration-200 ease-out group-hover:translate-x-12"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          fill="none"
                          class="w-5 h-5 text-yellow-400"
                        >
                          <path
                            d="M14 5l7 7m0 0l-7 7m7-7H3"
                            stroke-width="2"
                            stroke-linejoin="round"
                            stroke-linecap="round"
                          ></path>
                        </svg>
                      </span>
                      <span
                        class="absolute left-0 pl-2.5 -translate-x-12 group-hover:translate-x-0 ease-out duration-200"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          fill="none"
                          class="w-5 h-5 text-yellow-400"
                        >
                          <path
                            d="M14 5l7 7m0 0l-7 7m7-7H3"
                            stroke-width="2"
                            stroke-linejoin="round"
                            stroke-linecap="round"
                          ></path>
                        </svg>
                      </span>
                      <span
                        class="relative w-full text-left transition-colors duration-200 ease-in-out group-hover:text-white dark:group-hover:text-gray-200"
                        >Get Started</span>
                    </div>
                  </div>
                </a>
                </div>
                
            </div>
            
        </div>
    </div>
  );
};

export default Hero;

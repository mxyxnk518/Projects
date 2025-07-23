import React from 'react'

const Cards = () => {
  return (
    <div >
        <h1 className="mb-5 text-5xl font-bold flex justify-center pt-10">What We offer</h1>
        <div className='flex justify-center p-10 mb-10 lg:grid-cols-4 sm:grid grid-cols-2 gap-5'>
            <div class=" rounded-2xl shadow-sm ">
                <div class="group overflow-hidden relative after:duration-500 before:duration-500  duration-500 hover:after:duration-500 hover:after:translate-x-24 hover:before:translate-y-12 hover:before:-translate-x-32 hover:duration-500 after:absolute after:w-24 after:h-24 after:bg-yellow-700 after:rounded-full  after:blur-xl after:bottom-32 after:right-16 after:w-12 after:h-12  before:absolute before:w-20 before:h-20 before:bg-yellow-400 before:rounded-full  before:blur-xl before:top-20 before:right-16 before:w-12 before:h-12  hover:rotate-12 flex justify-center items-center h-56 w-80 origin-bottom-right bg-neutral-900 rounded-2xl outline outline-slate-400 -outline-offset-8">
                    <div class="z-10 flex flex-col items-center gap-2">
                        <span class="text-slate-400 text-2xl  font-bold"> Discover Our<span className='text-amber-400'> Exclusive</span> <p className='flex justify-center'>Travel Solutions</p> </span>
                        <p class="text-gray-50 text-sm">Explore a suite of specialized travel services<p className='flex justify-center'> designed to enhance your journey.</p></p>
                    </div>
                </div>
            </div>
            <div class=" rounded-2xl shadow-sm ">
                <div class="group overflow-hidden relative after:duration-500 before:duration-500  duration-500 hover:after:duration-500 hover:after:translate-x-24 hover:before:translate-y-12 hover:before:-translate-x-32 hover:duration-500 after:absolute after:w-24 after:h-24 after:bg-yellow-700 after:rounded-full  after:blur-xl after:bottom-32 after:right-16 after:w-12 after:h-12  before:absolute before:w-20 before:h-20 before:bg-yellow-400 before:rounded-full  before:blur-xl before:top-20 before:right-16 before:w-12 before:h-12  hover:rotate-12 flex justify-center items-center h-56 w-80 origin-bottom-right bg-neutral-900 rounded-2xl outline outline-slate-400 -outline-offset-8">
                    <div class="z-10 flex flex-col items-center gap-2">
                        <span class="text-slate-400 text-2xl font-bold">Explore <span className='text-amber-400'> Flights </span>with Ease </span>
                        <p class="text-gray-50 text-sm ml-5">Browse through a wide selection of flights tailored to your preferences, then  book<p className='flex justify-center'> with just a click.</p></p>
                    </div>
                </div>
            </div>
            <div class=" rounded-2xl shadow-sm ">
                <div class="group overflow-hidden relative after:duration-500 before:duration-500  duration-500 hover:after:duration-500 hover:after:translate-x-24 hover:before:translate-y-12 hover:before:-translate-x-32 hover:duration-500 after:absolute after:w-24 after:h-24 after:bg-yellow-700 after:rounded-full  after:blur-xl after:bottom-32 after:right-16 after:w-12 after:h-12  before:absolute before:w-20 before:h-20 before:bg-yellow-400 before:rounded-full  before:blur-xl before:top-20 before:right-16 before:w-12 before:h-12  hover:rotate-12 flex justify-center items-center h-56 w-80 origin-bottom-right bg-neutral-900 rounded-2xl outline outline-slate-400 -outline-offset-8">
                    <div class="z-10 flex flex-col items-center gap-2">
                        <span class="text-slate-400 text-2xl font-bold">Explore with <span className='text-amber-400'> Interactive </span> <p className='flex justify-center'>Maps</p> </span>
                        <p class="text-gray-50 text-sm">Navigate seamlessly through destinations <p className='flex justify-center'> with our integrated mapping feature.</p></p>
                    </div>
                </div>
            </div>
            <div class=" rounded-2xl shadow-sm ">
                <div class="group overflow-hidden relative after:duration-500 before:duration-500  duration-500 hover:after:duration-500 hover:after:translate-x-24 hover:before:translate-y-12 hover:before:-translate-x-32 hover:duration-500 after:absolute after:w-24 after:h-24 after:bg-yellow-700 after:rounded-full  after:blur-xl after:bottom-32 after:right-16 after:w-12 after:h-12  before:absolute before:w-20 before:h-20 before:bg-yellow-400 before:rounded-full  before:blur-xl before:top-20 before:right-16 before:w-12 before:h-12  hover:rotate-12 flex justify-center items-center h-56 w-80 origin-bottom-right bg-neutral-900 rounded-2xl outline outline-slate-400 -outline-offset-8">
                    <div class="z-10 flex flex-col items-center gap-2">
                        <span class="text-slate-400 text-2xl font-bold">Get Plans <span className='text-amber-400'>  According </span>to <p className='flex justify-center'>Your Budget</p> </span>
                        <p class="text-gray-50 text-sm">Find the best travel options that fit your <p className='flex justify-center'>  budget and preferences.</p></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Cards

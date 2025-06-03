import React, { useState } from 'react';
import AiwithText from '../components/AiwithText';
import AiwithImage from '../components/AiwithImage';

const Home = () => {
  const [aiWith, setLAiWith] = useState('text');

  const handleAiWith = (value) => {
    setLAiWith(value);
  }

  return (
    <div>
      <h1 className='font-bold text-5xl'>PlateSense:<p> A <span className='text-lime-400'>Generative</span> AI Restaurant App! </p></h1>

      <div className='m-5'>
        <button
          onClick={() => handleAiWith('text')}
          className={aiWith == 'text' ? 'aiWithActive' : 'm-2 hover:bg-lime-800'}>
          AI with Text
        </button>

        <button  
          className={aiWith == 'image' ? 'aiWithActive' : 'm-2 hover:bg-lime-800'}
          onClick={() => handleAiWith('image')}>
          AI with Image
        </button>
      </div>

      {
        aiWith == 'text' ?
          <AiwithText />
          :
          <AiwithImage />
      }
    </div>
  );
};

export default Home;
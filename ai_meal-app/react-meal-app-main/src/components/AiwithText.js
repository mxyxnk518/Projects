import React, { useState } from 'react';
import { GoogleGenerativeAI } from "@google/generative-ai";

const AiwithText = () => {
    const genAI = new GoogleGenerativeAI('AIzaSyA773JLaxD_jX71eLgvSFqw2EzJ4-u6AJc');

    const [search, setSearch] = useState('');
    const [aiResponse, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    
    async function aiRun() {
        setLoading(true);
        setResponse('');
        const model = genAI.getGenerativeModel({ model: "gemini-pro" });
        const prompt = `Hey AI, I'm craving something delicious! Can you recommend a mouthwatering meal in the ${search} category? Feel free to include details like ingredients, preparation methods, and any special prices or offers give the data where each new subheading and heading are seperated and are in seperate lines`;
        const result = await model.generateContent(prompt);
        const response = await result.response;
        let text = response.text();
        text = text.replaceAll("*", " ");
        setResponse(text);
        setLoading(false);
    }

    const handleChangeSearch = (e) => {
        setSearch(e.target.value);
    }

    const handleClick = () => {
        aiRun();
    }

    return (
        <div>
            <div className='flex'>
                <input placeholder='Search Food with Category using Generative AI' onChange={(e) => handleChangeSearch(e)} />
                <button className='ml-5 bg-lime-400 hover:bg-lime-600' onClick={() => handleClick()}>Search</button>
            </div>

            {
                loading == true && (aiResponse == '') ?
                    <p className='m-10'>Loading ...</p>
                    :
                    <div className='m-10'>
                        <p>{aiResponse}</p>
                    </div>
            }
        </div>
    );
};

export default AiwithText;
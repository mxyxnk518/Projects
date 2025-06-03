import React from 'react';

const About = () => {
  return (
    <div className="bg-gray-100 py-16">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 text-center">Welcome to PlateSense</h1>
        <p className="text-lg mb-6 text-center text-gray-800">
          Our Restaurant is not just a place to enjoy delicious food, but also a hub for culinary exploration and innovation. Our website offers exciting features to enhance your dining experience:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">Dish Information Generator</h2>
            <p className="text-lg text-gray-800 mb-4">
              Enter the name of any dish, and our AI system will provide you with detailed information about its ingredients, preparation methods, and serving suggestions. Whether you're a food enthusiast or a curious diner, this feature will satisfy your culinary curiosity.
            </p>
            <p className="text-lg text-gray-800">
              Start exploring our extensive database of dishes and uncover fascinating insights into your favorite foods.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">Image Recognition</h2>
            <p className="text-lg text-gray-800 mb-4">
              Can't quite put a name to that dish you enjoyed at a friend's dinner party or a restaurant? Upload an image, and our advanced AI technology will analyze it to identify the dish and provide you with relevant information.
            </p>
            <p className="text-lg text-gray-800">
              Never wonder about a dish again - let our image recognition feature satisfy your curiosity and enhance your dining experiences.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;

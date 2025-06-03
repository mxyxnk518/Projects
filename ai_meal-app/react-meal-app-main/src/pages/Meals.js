import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { API_BASE_URL } from '../core/config';
import { addToFavourites } from '../state/slices/favouriteSlice';

const Meals = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();

  const [category, setCategory] = useState(location?.state?.category);
  const [meals, setMeals] = useState([]);

  useEffect(() => {
    if (!location?.state?.category) {
      navigate('/menu');
    }

    const fetchMeals = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/1/filter.php?c=${category?.strCategory}`);
        setMeals(response.data.meals);
      } catch (error) {
        console.error('Error fetching meals:', error);
      }
    };

    fetchMeals();
  }, [category]);

  const handleFavorite = (meal) => {
    console.log('Meal marked as favorite:', meal);
    dispatch(addToFavourites(meal));
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className='text-center mb-4'>Meals in the category: {category?.strCategory}</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {meals && meals.map((meal) => (
          <div className="bg-white rounded-lg shadow-md" key={meal.idMeal}>
            <img src={meal.strMealThumb} className="w-full h-48 object-cover rounded-t-lg" alt={meal.strMeal} />
            <div className="p-4">
              <h5 className="text-xl font-semibold mb-2">{meal.strMeal}</h5>
              <p className="text-gray-700 mb-2">Meal ID: {meal.idMeal}</p>
              <button onClick={() => handleFavorite(meal)} className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Mark as Favorite</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Meals;

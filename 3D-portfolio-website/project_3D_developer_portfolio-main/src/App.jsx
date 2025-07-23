import { BrowserRouter } from "react-router-dom";
import { Link as ScrollLink, Element } from 'react-scroll'; 
import { About, Contact, Experience, Feedbacks, Hero, Navbar, Tech, Works, StarsCanvas } from "./components";

const App = () => {
  return (
    <BrowserRouter>
      <div className='relative z-0 bg-primary'>
        <StarsCanvas />
        
        <Navbar />
        <Hero />
        
        <About />
        <Experience />
        <Tech />
        <Works />
        <Feedbacks />
        <div className='relative z-0'>
          <Contact />
          
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;

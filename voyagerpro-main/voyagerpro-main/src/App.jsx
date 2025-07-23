import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import { ParallaxProvider, Parallax } from 'react-scroll-parallax'; // Import ParallaxProvider
import { SignIn, SignUp, Hero, Navbar, Subscription, Footer, Generator, Cards, Faqs, Dashboard, Viewplan, Contact, AdminLogin, Admin, Message } from './components';

import { useInView } from 'react-intersection-observer';
import { Flight, StarsCanvas } from './components/canvas';

function FadeInSection({ children }) {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  return (
    <div ref={ref} className={`transition-opacity duration-1000 ${inView ? 'opacity-100' : 'opacity-0'}`}>
      {children}
    </div>
  );
}

function App() {
  return (
    <div className='justify-center items-center'>
      <Router>
       
        <ParallaxProvider>
          <Routes>
            <Route path="/signup" element={<SignUp style={{ backgroundColor: '#1a1a1a' }} />} />
            <Route path="/signin" element={<SignIn style={{ backgroundColor: '#222222' }} />} />
            <Route path='/dashboard' element={<Dashboard style={{ backgroundColor: '#333333' }} />} />
             <Route path='/admin/login' element={<AdminLogin />} />
            <Route path='/admin' element={<Admin />} />
            <Route path='/admin/view/message/:id' element={<Message />} />
            <Route path='/dashboard/view/:id' element={<Viewplan style={{ backgroundColor: '#333333' }} />} />
            <Route path="/" element={<>
              <ParallaxProvider>
                <Parallax speed={0}>
                  <FadeInSection>
                    <Navbar style={{ backgroundColor: '#1a1a1a' }} />
                  </FadeInSection>
                </Parallax>
                <Parallax speed={-5}>
                  <div className='grid grid-cols-2'>
                    <FadeInSection> 
                      <Flight style={{ backgroundColor: '#2a2a2a' }} />
                    </FadeInSection>
                    <FadeInSection> 
                      <Hero style={{ backgroundColor: '3a3a3a' }} />
                    </FadeInSection>
                  </div>
                </Parallax>
                <Parallax speed={10}>
                  <FadeInSection>
                    <Cards style={{ backgroundColor: '#1a1a1a' }} />
                  </FadeInSection>
                </Parallax>
                <Parallax speed={0}>
                  <FadeInSection>
                    <Subscription style={{ backgroundColor: '#222222' }} />
                  </FadeInSection>
                </Parallax>
                <Parallax speed={10}>
                  <FadeInSection>
                    <Faqs style={{ backgroundColor: '#333333' }} />
                  </FadeInSection>
                </Parallax>
                <Parallax speed={-5}>
                  <FadeInSection>
                    <Contact style={{ backgroundColor: '#1a1a1a' }} />
                  </FadeInSection>
                </Parallax>
                <Parallax speed={0}>
                  <FadeInSection>
                    <Footer style={{ backgroundColor: '#222222' }} />
                  </FadeInSection>
                </Parallax>
              </ParallaxProvider>
            </>} />
            <Route path='/generator' element={<>
              <div className=''>
                <Navbar style={{ backgroundColor: '#1a1a1a' }} />
                <Generator />
              </div>
            </>} />
          </Routes>
        </ParallaxProvider>

      </Router>
    </div>
  );
}

export default App;

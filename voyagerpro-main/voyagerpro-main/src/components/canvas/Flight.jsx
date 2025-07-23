import React, { useRef, useEffect } from 'react';
import { Canvas, useLoader } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from '@react-three/drei';
import * as TWEEN from '@tweenjs/tween.js';
import { useWindowSize } from 'react-use';

const Model = () => {
  const { scene } = useLoader(GLTFLoader, '/flight_model/scene.gltf');
  return (
    <group>
      <primitive object={scene} position={[-2, 0, -5]} />
    </group>
  );
};

const Flight = () => {
  const flightRef = useRef();
  const { width, height } = useWindowSize();

  useEffect(() => {
    const scaleFactor = Math.min(width / 6000, height / 6000); 
    const tween = new TWEEN.Tween({ x: -2, z: -5, scale: scaleFactor, rotationz: Math.PI / 2 })
      .to({ x: 0, z: 3, scale: scaleFactor, rotationz: 0 }, 2000) 
      .onUpdate((coords) => {
        if (flightRef.current) {
          flightRef.current.position.x = coords.x;
          flightRef.current.position.z = coords.z;
          flightRef.current.scale.set(coords.scale, coords.scale, coords.scale);
          flightRef.current.rotation.z = coords.rotationz;
        }
      })
      .start();

    const animate = () => {
      requestAnimationFrame(animate);
      TWEEN.update();
    };
    animate();

    return () => {
      tween.stop();
    };
  }, [width, height]);

  return (
    <div style={{ width: '100vw', height: '100vh' }}> 
      <Canvas style={{ background: '#000' }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <pointLight position={[-10, -10, -5]} intensity={0.5} />
        <OrbitControls 
          enableZoom={false}
        />
        <group ref={flightRef}>
          <Model />
        </group>
        <camera position={[0, 0, 10]} /> 
      </Canvas>
    </div>
  );
};

export default Flight;

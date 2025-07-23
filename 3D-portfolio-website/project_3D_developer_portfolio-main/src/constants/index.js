import {
  mobile,
  backend,
  creator,
  web,
  javascript,
  typescript,
  aws,
  cloud,
  html,
  css,
  lyriks,
  prepersona,
  reactjs,
  python,
  tailwind,
  flask,
  c,
  git,
  figma,
  django,
  meta,
  starbucks,
  tesla,
  shopify,
  voyagepro,
  jobit,
  tripguide,
  threejs,
} from "../assets";

export const navLinks = [
  {
    id: "about",
    title: "About",
  },
  {
    id: "work",
    title: "Work",
  },
  {
    id: "contact",
    title: "Contact",
  },
];

const services = [
  {
    title: "Web Developer",
    icon: web,
  },
  {
    title: "React Native Developer",
    icon: mobile,
  },
  {
    title: "Cloud Computing",
    icon: backend,
  },
  {
    title: "Python Devoloper",
    icon: creator,
  },
];

const technologies = [
  {
    name: "HTML 5",
    icon: html,
  },
  {
    name: "CSS 3",
    icon: css,
  },
  {
    name: "JavaScript",
    icon: javascript,
  },
  {
    name: "TypeScript",
    icon: typescript,
  },
  {
    name: "React JS",
    icon: reactjs,
  },
  {
    name: "Python",
    icon: python,
  },
  {
    name: "Tailwind CSS",
    icon: tailwind,
  },
  {
    name: "Flask",
    icon: flask,
  },
  {
    name: "C#",
    icon: c,
  },
  {
    name: "Three JS",
    icon: threejs,
  },
  {
    name: "git",
    icon: git,
  },
  {
    name: "aws",
    icon: aws,
  },
  {
    name: "django",
    icon: django,
  },
];

const experiences = [
  {
    title: "Html Css and Javascript",
    icon: starbucks,
    iconBg: "#E6DEDD",
    
    points: [
      "Learning Html and Css from a formal education as well as having an online certification to prove my knowledge with these tools",
      "Developing and maintaining static web applications using Html Css Javascript",
      "Making a variety of projects for reputable companies",
      "Implementing responsive design and ensuring cross-browser compatibility.",
      
    ],
  },
  {
    title: "React Native devoloper",
    
    icon: tesla,
    iconBg: "#E6DEDD",
    
    points: [
      "Developing and maintaining web applications using React.js and other related technologies.",
      "Collaborating with cross-functional teams including designers and other developers to create high-quality products.",
      "Making real world applications using react",
      "Participating and contributing in open source projects",
    ],
  },
  {
    title: "Python Devoloper",
    
    icon: shopify,
    iconBg: "#E6DEDD",
    
    points: [
      "Developed robust and scalable Python backend solutions, leveraging frameworks such as Django and Flask to deliver efficient and reliable web applications.",
      "Applied expertise in database design and optimization, ensuring seamless data management and retrieval for enhanced application performance.",
      "Collaborated with cross-functional teams to implement RESTful APIs, contributing to the development of interactive and responsive user interfaces.",
      "Continuously improved system functionality through debugging, optimization, and integration of innovative technologies, demonstrating a commitment to staying current with industry best practices.",
    ],
  },
  {
    title: "Full stack Developer",
    
    icon: meta,
    iconBg: "#E6DEDD",
    
    points: [
      "Proficient in full-stack development, seamlessly integrating Python for backend logic and React for dynamic and responsive user interfaces, resulting in well-rounded web applications.",
      "Designed and implemented RESTful APIs using Python-based frameworks (Django/Flask) to establish robust communication between the frontend and backend, ensuring optimal data flow.",
      "Collaborated on end-to-end development cycles, leveraging Python's versatility for backend services and React's component-driven architecture for building modern and engaging user experiences.",
      "Maintained a holistic approach to software development, from database design and server-side logic in Python to crafting intuitive user interfaces with React, delivering cohesive and feature-rich applications.",

    ],
  },
  
  {
    title: "Cloud Computing & AWS Practitioner",

    icon: cloud,
    iconBg: "#E6DEDD",

    points: [
      "Deployed full-stack applications using cloud platforms including AWS, Vercel, and GitHub Pages, ensuring performance, scalability, and global reach.",
      "Configured and managed AWS services such as S3 (static hosting), EC2 (custom deployments), and Route 53 (domain routing) for production-ready applications.",
      "Integrated environment variables, IAM roles, and access controls to maintain secure and efficient cloud infrastructure during development and deployment.",
      "Utilized CI/CD pipelines and GitHub Actions to automate build, test, and deploy workflows with cloud endpoints for seamless version control and delivery.",
      "Explored AWS Lambda for serverless functions and backend logic, improving scalability and reducing infrastructure overhead across select projects."
    ],
  }

];


const projects = [
  {
    name: "VoyagePro",
    description:
      "VoyagePro is a dynamic travel planning application that builds a complete trip itinerary tailored to the user's preferences. Using a clean React frontend paired with a pure JavaScript backend, the app prompts the user for key travel details — destination, dates, travel type, and activity preferences — and instantly generates a detailed multi-day schedule.",
    tags: [
      {
        name: "React",
        color: "blue-text-gradient",
      },
      {
        name: "JSX",
        color: "green-text-gradient",
      },
      {
        name: "Tailwind",
        color: "pink-text-gradient",
      },
    ],
    image: voyagepro,
    source_code_link: " https://github.com/mxyxnk518/Projects/tree/main/voyagerpro-main/voyagerpro-main",
  },
  {
    name: "Pre Persona",
    description:
      "PrePersona is an advanced AI-powered digital clone application that learns and mimics your personal communication style, decision-making patterns, and thought processes. It creates a personalized AI representation that can predict how you would respond to future scenarios.",
    tags: [
      {
        name: "Streamlit",
        color: "blue-text-gradient",
      },
      {
        name: "Groq API",
        color: "green-text-gradient",
      },
      {
        name: "LangChain",
        color: "pink-text-gradient",
      },
    ],
    image: prepersona,
    source_code_link: "https://github.com/mxyxnk518/Projects/tree/main/DataInsightPro",
  },
  {
    name: "Lyriks",
    description:
      "Lyriks is a sleek, responsive music streaming platform that replicates the look, feel, and experience of Spotify. Built entirely with modern frontend frameworks and real-time APIs, it allows users to explore trending songs, view synchronized lyrics, and stream music directly through an elegant UI.",
    tags: [
      {
        name: "Tailwind",
        color: "blue-text-gradient",
      },
      {
        name: "Redux",
        color: "green-text-gradient",
      },
      {
        name: "RapidAPI",
        color: "pink-text-gradient",
      },
    ],
    image: lyriks,
    source_code_link: "https://github.com/mxyxnk518/Projects/tree/main/project_music_player-main",
  },
];

export { services, technologies, experiences, projects };

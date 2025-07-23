import {
  mobile,
  backend,
  creator,
  web,
  javascript,
  typescript,
  html,
  css,
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
  carrent,
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
    title: "Unity Game Devoloper",
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
    name: "figma",
    icon: figma,
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
    date: "March 2020 - April 2021",
    points: [
      "Learning Html and Css from a formal education as well as having an online certification to prove my knowledge with these tools",
      "Developing and maintaining static web applications using Html Css Javascript",
      "Making a variety of projects for reputable companies",
      "Implementing responsive design and ensuring cross-browser compatibility.",
      
    ],
  },
  {
    title: "React Native devoloper",
    company_name: "Tesla",
    icon: tesla,
    iconBg: "#E6DEDD",
    date: "Jan 2021 - Feb 2022",
    points: [
      "Developing and maintaining web applications using React.js and other related technologies.",
      "Collaborating with cross-functional teams including designers and other developers to create high-quality products.",
      "Making real world applications using react",
      "Participating and contributing in open source projects",
    ],
  },
  {
    title: "Python Devoloper",
    company_name: "Shopify",
    icon: shopify,
    iconBg: "#E6DEDD",
    date: "Jan 2022 - Jan 2023",
    points: [
      "Developed robust and scalable Python backend solutions, leveraging frameworks such as Django and Flask to deliver efficient and reliable web applications.",
      "Applied expertise in database design and optimization, ensuring seamless data management and retrieval for enhanced application performance.",
      "Collaborated with cross-functional teams to implement RESTful APIs, contributing to the development of interactive and responsive user interfaces.",
      "Continuously improved system functionality through debugging, optimization, and integration of innovative technologies, demonstrating a commitment to staying current with industry best practices.",
    ],
  },
  {
    title: "Full stack Developer",
    company_name: "Meta",
    icon: meta,
    iconBg: "#E6DEDD",
    date: "Jan 2023 - Present",
    points: [
      "Proficient in full-stack development, seamlessly integrating Python for backend logic and React for dynamic and responsive user interfaces, resulting in well-rounded web applications.",
      "Designed and implemented RESTful APIs using Python-based frameworks (Django/Flask) to establish robust communication between the frontend and backend, ensuring optimal data flow.",
      "Collaborated on end-to-end development cycles, leveraging Python's versatility for backend services and React's component-driven architecture for building modern and engaging user experiences.",
      "Maintained a holistic approach to software development, from database design and server-side logic in Python to crafting intuitive user interfaces with React, delivering cohesive and feature-rich applications.",

    ],
  },
];

const testimonials = [
  {
    testimonial:
      "I thought it was impossible to make a website as beautiful as our product, but Rick proved me wrong.",
    name: "Sara Lee",
    designation: "CFO",
    company: "Acme Co",
    image: "https://randomuser.me/api/portraits/women/4.jpg",
  },
  {
    testimonial:
      "I've never met a web developer who truly cares about their clients' success like Rick does.",
    name: "Chris Brown",
    designation: "COO",
    company: "DEF Corp",
    image: "https://randomuser.me/api/portraits/men/5.jpg",
  },
  {
    testimonial:
      "After Rick optimized our website, our traffic increased by 50%. We can't thank them enough!",
    name: "Lisa Wang",
    designation: "CTO",
    company: "456 Enterprises",
    image: "https://randomuser.me/api/portraits/women/6.jpg",
  },
];

const projects = [
  {
    name: "Car Rent",
    description:
      "Web-based platform that allows users to search, book, and manage car rentals from various providers, providing a convenient and efficient solution for transportation needs.",
    tags: [
      {
        name: "react",
        color: "blue-text-gradient",
      },
      {
        name: "mongodb",
        color: "green-text-gradient",
      },
      {
        name: "tailwind",
        color: "pink-text-gradient",
      },
    ],
    image: carrent,
    source_code_link: "https://github.com/",
  },
  {
    name: "Job IT",
    description:
      "Web application that enables users to search for job openings, view estimated salary ranges for positions, and locate available jobs based on their current location.",
    tags: [
      {
        name: "react",
        color: "blue-text-gradient",
      },
      {
        name: "restapi",
        color: "green-text-gradient",
      },
      {
        name: "scss",
        color: "pink-text-gradient",
      },
    ],
    image: jobit,
    source_code_link: "https://github.com/",
  },
  {
    name: "Trip Guide",
    description:
      "A comprehensive travel booking platform that allows users to book flights, hotels, and rental cars, and offers curated recommendations for popular destinations.",
    tags: [
      {
        name: "nextjs",
        color: "blue-text-gradient",
      },
      {
        name: "supabase",
        color: "green-text-gradient",
      },
      {
        name: "css",
        color: "pink-text-gradient",
      },
    ],
    image: tripguide,
    source_code_link: "https://github.com/",
  },
];

export { services, technologies, experiences, testimonials, projects };

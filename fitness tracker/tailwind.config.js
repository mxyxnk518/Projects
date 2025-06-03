/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        darkslateblue: "#1f305c",
        black: "#000",
        slategray: "#667b95",
        gray: {
          "100": "#fbffff",
          "200": "#f9fdfe",
          "300": "rgba(0, 0, 0, 0.2)",
        },
        lightslategray: "#909fb9",
        steelblue: "#3d4f76",
        white: "#fff",
        lavender: "#d4edff",
      },
      spacing: {},
      fontFamily: {
        "inria-sans": "'Inria Sans'",
      },
      borderRadius: {
        "41xl": "60px",
        "39xl": "58px",
        "23xl": "42px",
        "25xl": "44px",
      },
    },
    fontSize: {
      "17xl": "36px",
      xl: "20px",
      base: "16px",
      inherit: "inherit",
    },
    screens: {
      mq500: {
        raw: "screen and (max-width: 500px)",
      },
      mq450: {
        raw: "screen and (max-width: 450px)",
      },
    },
  },
  corePlugins: {
    preflight: false,
  },
};

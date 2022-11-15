/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts}"],
  theme: {
    colors:{
      'dark':{
        'violet':{
          100: "#000000",
          200: "#150050",
          300: "#3F0071"
        }
      }
    }
  },
  plugins: [],
};

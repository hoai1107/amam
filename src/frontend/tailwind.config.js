/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts}"],
  theme: {
    colors: {
      blueSky: {
        light: {
          800: "#e8fcff",
        },
        DEFAULT: "#8cf2ff",
        dark: {
          100: "#7edae6",
          200: "#70c2cc",
          300: "#62a9b3",
          400: "#549199",
          500: "#467980",
          600: "#386166",
          700: "#2a494c",
          800: "#1c3033",
        },
      },
      yellow: {
        DEFAULT: "#ffef8c",
        light: {
          800: "#fffce8",
        },
      },
      red: "#e33232",
      blue: "#5c5cf0",
      black: "#000000",
      white: "#ffffff",
      gray: {
        100: "#e6e6e6",
        300: "#b3b3b3",
        400: "#999999",
      },
    },
    fontFamily: {
      sans: ["Readex Pro", "sans-serif"],
    },
    fontSize: {
      xxs: ["11px", "16px"],
      xs: ["12px", "16px"],
      sm: ["14px", "20px"],
      base: ["16px", "24px"],
      lg: ["20px", "32px"],
      xl: ["24px", "36px"],
      "2xl": ["32px", "48px"],
      "3xl": ["48px", "64px"],
      "4xl": ["64px", "80px"],
    },
    borderRadius: {
      DEFAULT: "8px",
    },
    boxShadow: {
      sm: "2px 2px #000000",
      md: "4px 4px #000000",
    },
    extend: {},
  },
  plugins: [],
};

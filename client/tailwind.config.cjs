/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors:{
        primaryRed: "#FF1A29",
        secondaryYellow: "#FFE700",
        primaryBlue: "#8761FF",
        secondaryPink: "#FF61D9"
      }
    },
  },
  plugins: [],
}

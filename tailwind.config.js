/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['templates/**/*.{html, js}'],
  theme: {
    extend: {
      container: {center: true}
    }
  },
  plugins: [require('@tailwindcss/typography')]
}

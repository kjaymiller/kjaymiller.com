/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['output/**/*.{html, js}'],
  theme: {
    extend: {
      container: {center: true}
    }
  },
  plugins: [require('@tailwindcss/typography')]
}

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html"],
    theme: {
      extend: {
        colors: {
          darkbg: 'var(--color-bg)',
          cardbg: 'var(--color-cardbg)',
          cardborder: 'var(--color-cardborder)',
          nregagreen: 'var(--color-accent)'
        }
      }
    },
    plugins: [],
  }
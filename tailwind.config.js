/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#6366f1',
        accent: '#f43f5e',
        dark: '#1e293b',
        light: '#f8fafc',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        indonesian: ['Noto Sans', 'sans-serif'],
        chinese: ['Noto Sans SC', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
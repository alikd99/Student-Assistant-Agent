/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        base:    '#0f1117',
        surface: '#161b27',
        card:    '#1a1f2e',
        border:  '#2a2f3e',
        primary: '#2563eb',
        'primary-hover': '#1d4ed8',
        muted:   '#64748b',
        text:    '#e8eaf0',
        subtle:  '#94a3b8',
      },
      fontFamily: {
        cairo: ['Cairo', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

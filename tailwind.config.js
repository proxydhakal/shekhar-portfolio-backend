/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './apps/portfolio/templates/**/*.html',
    './apps/blog/templates/**/*.html',
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        sand: '#DAD7CD',
        sage: '#A3B18A',
        leaf: '#588157',
        forest: '#3A5A40',
        pine: '#344E41',
        ink: '#344E41',
        muted: '#5C6B59',
        line: '#C9CFC0',
        paper: '#DAD7CD',
        night: '#344E41',
        panel: '#3A5A40',
        accent: {
          DEFAULT: '#588157',
          deep: '#3A5A40',
        },
      },
      backgroundImage: {
        theme: 'linear-gradient(120deg, #A3B18A 0%, #588157 42%, #3A5A40 78%, #344E41 100%)',
      },
      keyframes: {
        wash: {
          '0%': { transform: 'translate3d(0, 0, 0) scale(1)' },
          '100%': { transform: 'translate3d(0, -12px, 0) scale(1.04)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '0% 50%' },
          '100%': { backgroundPosition: '100% 50%' },
        },
      },
      animation: {
        wash: 'wash 12s ease-in-out infinite alternate',
        shimmer: 'shimmer 5s ease infinite alternate',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      maxWidth: {
        page: '72rem',
      },
    },
  },
  plugins: [],
};

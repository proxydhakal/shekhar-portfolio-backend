/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './apps/portfolio/templates/**/*.html',
    './apps/blog/templates/**/*.html',
    './templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Existing palette
        primary: '#6366f1',
        secondary: '#a855f7',
        accent: '#10b981',
        darkBg: '#020617',

        // Neon theme palette (used by home + blog neon templates)
        brand: '#00F5C4',
        brandpink: '#FF2D78',
        dark: '#050811',
        card: '#0C1120',
        border: '#1A2540',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
        poppins: ['Poppins', 'sans-serif'],
      },
      animation: {
        float: 'float 6s ease-in-out infinite',
        float2: 'float 8s ease-in-out infinite 2s',
        float3: 'float 7s ease-in-out infinite 4s',
        'spin-slow': 'spin 20s linear infinite',
        'pulse-slow': 'pulse 4s ease-in-out infinite',
        shimmer: 'shimmer 2s linear infinite',
        'gradient-x': 'gradient-x 4s ease infinite',
        'fade-up': 'fadeUp 0.7s ease both',
      },
      keyframes: {
        float: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-20px)' } },
        shimmer: { '0%': { backgroundPosition: '-200% center' }, '100%': { backgroundPosition: '200% center' } },
        'gradient-x': { '0%,100%': { backgroundPosition: '0% 50%' }, '50%': { backgroundPosition: '100% 50%' } },
        fadeUp: { '0%': { opacity: 0, transform: 'translateY(30px)' }, '100%': { opacity: 1, transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
};

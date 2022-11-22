/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')

const backfaceVisibility = plugin(function({addUtilities}) {
  addUtilities({
    '.backface-visible': {
      'backface-visibility': 'visible',
    },
    '.backface-hidden': {
      'backface-visibility': 'hidden',
    }
  })
});

const rotateY = plugin(function({addUtilities}) {
  addUtilities({
    '.flip-y': {
      transform: "rotateY(180deg)",
    },
    '.flip-y-30': {
      transform: "rotateY(30deg)",
    },
    '.flip-y-0': {
      transform: "rotateY(0)",
    }
  })
});

const preserve3d = plugin(function({addUtilities}) {
  addUtilities({
    '.preserve3d': {
      "transform-style": "preserve-3d"
    }
  })
});

const perspective = plugin(function({addUtilities}) {
  addUtilities({
    '.perspective-500': {
      "perspective": "800px"
    }
  })
});


module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors:{
        salsa: "#EE5454",
        mikado: "#FFC510",
        safety: "#F6DB35",
        un: "#4C94F6",
        neoblue: "#4C69F6"
      },
      keyframes: {
        dots: {
          '0%': {
            content: ''
        },
        '25%': {
            content: '.'
        },
        '50%': {
            content: '..'
        },
        '75%': {
            content: '...'
        },
        '100%': {
            content: ''
        },
        }
      },
      animation: {
        dots: "dots steps(1, end) 1s infinite"
      }
    },
  },
  plugins: [backfaceVisibility, rotateY, preserve3d, perspective],
}

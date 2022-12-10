/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');

const clipPath = plugin(function ({ addUtilities }) {
	addUtilities({
		'.clip-path': {
			'clip-path': 'polygon(100% 75%, 50% 100%, 0 75%, 0 0, 100% 0)'
		}
	});
});

const backfaceVisibility = plugin(function ({ addUtilities }) {
	addUtilities({
		'.backface-visible': {
			'backface-visibility': 'visible'
		},
		'.backface-hidden': {
			'backface-visibility': 'hidden'
		}
	});
});

const rotateY = plugin(function ({ addUtilities }) {
	addUtilities({
		'.flip-y': {
			transform: 'rotateY(180deg)'
		},
		'.flip-y-30': {
			transform: 'rotateY(30deg)'
		},
		'.flip-y-0': {
			transform: 'rotateY(0)'
		}
	});
});

const preserve3d = plugin(function ({ addUtilities }) {
	addUtilities({
		'.preserve3d': {
			'transform-style': 'preserve-3d'
		}
	});
});

const perspective = plugin(function ({ addUtilities }) {
	addUtilities({
		'.perspective-500': {
			perspective: '800px'
		}
	});
});

module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				space: '#293462',
				cornflower: '#313F78',
				lemon: '#FFF80A',
				ua: '#D61C4E',
				spaceh: '#313F76',
				cornflowerh: '#39498B',
				lemonh: '#FFFA76',
				uah: '#E22356'
			},
			keyframes: {
				dots: {
					'0%': {
						content: "''"
					},
					'25%': {
						content: "'.'"
					},
					'50%': {
						content: "'..'"
					},
					'75%': {
						content: "'...'"
					},
					'100%': {
						content: "''"
					}
				},
				yspin: {
					'0%': {
						transform: 'rotateY(0deg)'
					},
					'100%': {
						transform: 'rotateY(360deg)'
					}
				}
			},
			animation: {
				dots: 'dots steps(1, end) 2s infinite',
				yspin: 'yspin 3s linear infinite'
			}
		}
	},
	plugins: [backfaceVisibility, rotateY, preserve3d, perspective, clipPath]
};

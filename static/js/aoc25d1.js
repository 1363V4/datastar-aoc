import { waapi } from 'https://cdn.jsdelivr.net/npm/animejs/+esm';

export function spin (deg) {
	waapi.animate("#lock", {
		rotateZ: '100deg',
		duration: 1000,
	});
}

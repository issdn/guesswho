// type params = { isGuessing: boolean, isPicking: boolean, callback: () => void };

export const conditionalhandler = (node: HTMLElement, callback: (e: Event) => void) => {
	const clickHandler = (callback: (e: Event) => void) => {
		node.addEventListener('click', callback);
	};

	clickHandler(callback);

	return {
		update(newCallback: (e: Event) => void) {
			node.removeEventListener('click', callback);
			clickHandler(newCallback);
		},
		destroy() {
			node.removeEventListener('click', callback);
		}
	};
};

export const shadowhandler = (node: HTMLElement, shouldDropShadow: boolean) => {
	const handleMouseEnter = () => {
		if (shouldDropShadow) {
			node.dispatchEvent(new CustomEvent('shadowenter'));
		}
	};

	const handleMouseLeave = () => {
		if (shouldDropShadow) {
			node.dispatchEvent(new CustomEvent('shadowleave'));
		}
	};

	node.addEventListener('mouseenter', handleMouseEnter, true);
	node.addEventListener('mouseleave', handleMouseLeave, true);

	return {
		update(newShouldDropShadow: boolean) {
			shouldDropShadow = newShouldDropShadow;
			handleMouseEnter();
			handleMouseLeave();
		},
		destroy() {
			node.removeEventListener('mouseenter', handleMouseEnter, true);
			node.removeEventListener('mouseleave', handleMouseLeave, true);
		}
	};
};

document.addEventListener("DOMContentLoaded", () => {
	const moduleNameRegex = /(qctrl)|\./gi;
	const h2ModuleNames = document.querySelectorAll("h2").filter(element => {
		const elText = element.innerText;
		return moduleNameRegex.test(elText);
	});
	console.log(h2ModuleNames);
});

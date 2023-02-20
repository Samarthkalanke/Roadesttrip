const options = {
	method: 'GET',
	headers: {
		'X-RapidAPI-Key': '8e39206459msh63119b14325b472p1a320bjsnac696cb1d4af',
		'X-RapidAPI-Host': 'car-data.p.rapidapi.com'
	}
};

fetch('https://car-data.p.rapidapi.com/cars?limit=10&page=0', options)
	.then(response => response.json())
	.then(response => console.log(response))
	.catch(err => console.error(err));
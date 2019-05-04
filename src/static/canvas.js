window.addEventListener("load", () => {

	const canvas = document.querySelector('#canvas');
	const ctx = canvas.getContext('2d');

	console.log("hi!")

	canvas.height = 300;
	canvas.width = 300;

	let painting = false;

	function startPosition(e){
		painting = true;
		draw(e);
	}

	function endPosition(){
		painting = false;
		ctx.beginPath();

		var imageData = ctx.getImageData(0, 0, 300, 300).data;

		let  threshold = 200;

		/*for (var i = 0; i < imageData.length; i+=4) {
  			imageData[i] = imageData[i+1] = imageData[i+2] = imageData[i] > threshold ? 255 : 0;
		}*/

		console.log(imageData);


		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/draw/', true);
		//xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

		xhr.send(imageData);
		/*xhr.send(JSON.stringify({
		    value: imgData
		}));*/


	}

	function draw(e) {
		
		if (!painting) return;

		ctx.lineWidth = 10;
		ctx.lineCap = 'round';

		ctx.lineTo(e.clientX, e.clientY);
		ctx.stroke();

		ctx.beginPath();
		ctx.moveTo(e.clientX, e.clientY);
	}

	canvas.addEventListener("mousedown",startPosition);
	canvas.addEventListener("mouseup",endPosition);
	canvas.addEventListener("mousemove",draw);
});
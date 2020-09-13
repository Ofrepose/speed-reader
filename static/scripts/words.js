current_memory = [];

var paused = false;

memIterCur = 0;

memIterTot = 3;

var totMemoriesDone = 0;

$(function() {
	$("#unpause").hide();
});

function changeFont(whatItDoTho) {
	let fontGrabber = document.getElementById("lst");
	let style = window
		.getComputedStyle(fontGrabber, null)
		.getPropertyValue("font-size");
	let fontSize = parseFloat(style);

	whatItDoTho === "increase"
		? (fontGrabber.style.fontSize = fontSize + 3 + "px")
		: whatItDoTho === "decrease"
		? (fontGrabber.style.fontSize = fontSize - 3 + "px")
		: null;
}

function savePage() {
	pauseRead();
	document.getElementById("name").value = amt;

	var form = document.getElementById("pageSave");
	form.submit();
}

function slowDown() {
	pauseRead();
	$("#top").css("opacity", "0");
	setTimeout(function() {
		speed = speed + 100;
		setTimeout(function() {
			unpauseRead();
			$("#top").css("opacity", "1");
		}, 10);
	}, speed + 1);
}

function speedUp() {
	pauseRead();
	$("#top").css("opacity", "0");
	setTimeout(function() {
		speed = speed - 100;
		setTimeout(function() {
			unpauseRead();
			$("#top").css("opacity", "1");
		}, 10);
	}, speed + 1);
}

function rewind() {
	pauseRead();
	setTimeout(function() {
		cur_content = p_content.slice(Math.max(p_content.length - 6));

		cur_needed = cur_content.slice(0, cur_content.length - 1).join(" ");

		cur_high = p_content.slice(Math.max(p_content.length - 1));

		$("#lst").html(
			cur_needed +
				" " +
				'<span style="background-color: red; opacity:.75;">' +
				cur_high +
				"</span>"
		);
		amt++;
		p_content.pop(p_content.length - 1);
		cur_content = [];
	}, 1);
}

function fastForward() {
	pauseRead();
	setTimeout(function() {
		let cur_content = [];
		let this_amt = amt;
		for (let i = 6; i > 0; i--) {
			cur_content.push(w_lst[this_amt - 1]);
			this_amt--;
		}
		cur_needed = cur_content.slice(0, cur_content.length - 1).join(" ");
		cur_high = p_content.slice(-1);
		$("#lst").html(cur_needed);
		amt--;
		p_content.push(p_content.length - 1);
		cur_content = [];
	}, 1);
}

function unpauseRead() {
	$("#unpause").hide();
	$("#pause").show();

	paused = false;

	timer(amt);
}

function pauseRead() {
	paused = true;

	$("#pause").hide();
	$("#unpause").show();
}

function stopTimer(amts) {
	amt = amts;
}

function memorize() {
	pauseRead();
	current_memory.push(w_lstPeriod[cur_Period - 1]);

	setTimeout(function() {
		memoryInit();
	}, 2000);
}

function memoryInit() {
	var memAmt = current_memory[0].split(" ").reverse().length - 1;
	var thisMem = current_memory[0].split(" ").reverse();
	var totMemoriesAmt = current_memory.length - 1;
	totMemoriesDone = 0;

	timer(memAmt);

	function timer(memAmt) {
		var timer = setInterval(function() {
			if (memAmt >= 0) {
				document.getElementById("lst").innerHTML = thisMem[memAmt];
			}

			if (memAmt <= 0 && memIterCur < memIterTot) {
				memIterCur = memIterCur + 1;
				memAmt = current_memory[totMemoriesDone].split(" ").reverse().length - 1;
			}

			if (
				memAmt == 0 &&
				memIterCur == memIterTot &&
				totMemoriesAmt != totMemoriesDone
			) {
				totMemoriesDone += 1;
				memAmt = current_memory[totMemoriesDone].split(" ").reverse().length - 1;
				memIterCur = 0;
			}

			memAmt--;
		}, speed);
	}
}

timer(amt);

function timer(amt) {
	while (w_lst === undefined) {
		return;
	}

	var timer = setInterval(async function() {
		if (amt >= 0) {
			document.getElementById("lst").innerHTML = w_lst[amt];

			p_content.push(w_lst[amt]);

			for (var i = w_lst[amt].length - 1; i >= 0; i--) {
				if (w_lst[amt][i] == ".") {
					cur_Period += 1;
				}
			}
		}

		if (paused) {
			clearInterval(timer);
			stopTimer(amt);
		}

		amt--;

	}, speed);
}

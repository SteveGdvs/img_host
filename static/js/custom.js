// code required when posting data with ajax
//taken from django doc
// using jQuery
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		let cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			let cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {

	let csrftoken = getCookie('csrftoken');

	$.ajaxSetup({
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	})
});
//end

//like ajax call
function like(image_id) {
	let btn_like = $('#like_' + image_id);
	let btn_dislike = $('#dislike_' + image_id);
	let score = $('#score_' + image_id);

	let data = {'image_id': image_id};
	$.ajax({
		url: '/vote/like/',
		data: data,
		type: 'POST',
	}).done(function (data) {
		console.log("like");
		console.log(data);
			if (data['action'] === 'remove') {
				btn_like.removeClass('text-success');
				score.text(data['score']);
			}
			if (data['action'] === 'add') {
				btn_like.addClass('text-success');
				btn_dislike.removeClass('text-danger');
				score.text(data['score']);
			}
		})
		.fail(function (data) {
			console.log('error in like func');
		});
}

//TODO HANDLE ERRORS
//dislike ajax call
function dislike(image_id) {
	let btn_like = $('#like_' + image_id);
	let btn_dislike = $('#dislike_' + image_id);
	let score = $('#score_' + image_id);
	let data = {'image_id': image_id};
	$.ajax({
		url: '/vote/dislike/',
		data: data,
		type: 'POST',
	}).done(function (data) {
		console.log("dislike");
		console.log(data);
			if (data['action'] === 'remove') {
				btn_dislike.removeClass('text-danger');
				score.text(data['score']);
			}
			if (data['action'] === 'add') {
				btn_dislike.addClass('text-danger');
				btn_like.removeClass('text-success');
				score.text(data['score']);
			}
		})
		.fail(function (data) {
			console.log('error in dislike func');
		});
}